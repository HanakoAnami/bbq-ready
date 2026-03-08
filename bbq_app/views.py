from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from .forms import SignupForm, EventForm, UserNameForm, UserEmailForm, EmailUpdateForm, BbqItemForm, ForgottenItemForm
from .models import Event, BbqItem, EventItem, Participant
from django.utils import timezone
from django.db.models import Q
from datetime import datetime
from django.views.generic import CreateView, UpdateView
from django.contrib import messages
from django.views.decorators.cache import never_cache
from django.db import models
from collections import defaultdict

def portfolio(request):
    return render(request, 'bbq_app/portfolio.html')

#ホームにイベントを３つまで表示
@never_cache
@login_required
def home(request):
    now = timezone.localtime()
    upcoming_events = (
        Event.objects
        .filter(user=request.user, held_at__gte=now)
        .order_by("held_at")[:3]
    )
    return render(request, 'bbq_app/home.html', {"upcoming_events": upcoming_events})

#ログイン
class UserLoginView(LoginView):
    template_name = 'bbq_app/login.html'
    
def signup(request):
    if request.method == "POST":
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # 登録後に自動ログイン
            return redirect('home')
    else:
        form = SignupForm()

    return render(request, 'bbq_app/signup.html', {'form': form})

#新規イベント作成
@login_required
def event_create(request):
    if request.method =="POST":
        form = EventForm(request.POST)
        if form.is_valid():
            event = form.save(commit=False)
            event.user = request.user
            event.save()
            
            Participant.objects.get_or_create(
                event=event, user=request.user, defaults={"name": request.user.first_name or request.user.username}
            )
            
            #共通テンプレ（user=None)+自分のテンプレをイベントにコピー
            templates = BbqItem.objects.filter(
                models.Q(user=request.user) | models.Q(user__isnull=True)
            )
            
            EventItem.objects.bulk_create([
                EventItem(event=event, bbq_item=template, is_selected=False, is_ready=False)
                for template in templates
            ])
            
            return redirect("item_edit", event_id=event.id)
    else:
        form = EventForm()
        
    return render(request, "bbq_app/event_form.html", {"form":form})

@login_required
def bbq_item_list_create(request):
    items = BbqItem.objects.filter(
        Q(user=request.user) | Q(user__isnull=True)).order_by("category", "name")
    
    if request.method == "POST":
        form = BbqItemForm(request.POST)
        if form.is_valid():
            bbq_item = form.save(commit=False)
            bbq_item.user = request.user
            bbq_item.save()
            return redirect("bbq_item_list_create")
        
    else:
        form = BbqItemForm()
            
    return render(
        request,
        "bbq_app/bbqitem_list_create.html",
        {"items":items, "form":form})


#イベント詳細
@login_required
def event_edit(request, event_id):
    event = get_object_or_404(Event, id=event_id, user=request.user)
    
    if request.method == "POST":
        form = EventForm(request.POST, instance=event)
        if form.is_valid():
            form.save()
            return redirect("item_edit", event_id=event.id)
    else:
        form = EventForm(instance=event)
    return render(request, "bbq_app/event_form.html", {"form": form, "event":event})
    

#持ち物編集リスト①
@login_required
def item_edit(request, event_id):
    event = get_object_or_404(Event, id=event_id, user=request.user)
    
    items = (
        EventItem.objects.filter(event=event).select_related("bbq_item").order_by("bbq_item__category", "bbq_item__name"))
    
    if request.method == "POST":
        selected_ids = set(request.POST.getlist("selected_items"))
        
        #チェック状態を保存
        for event_item in items:
            event_item.is_selected = str(event_item.id) in selected_ids
        EventItem.objects.bulk_update(items, ["is_selected"])
        return redirect("item_edit", event_id=event.id)
    
    grouped_dict =defaultdict(list)
    category_labels = dict(BbqItem.Category.choices)
    
    for event_item in items:
        grouped_dict[event_item.bbq_item.category].append(event_item)
        
    grouped_items = []
    for category, event_items in grouped_dict.items():
        grouped_items.append({
            "label": category_labels[category],
            "items": event_items,
        })  
    
    context = {
        "event": event,
        "grouped_items": grouped_items,
    }
    return render(request, "bbq_app/item_edit.html", context)


@login_required
def item_assign(request, event_id):
    event = get_object_or_404(Event, id=event_id, user=request.user)
    
    #このイベントの参加者(主催者も含めて)
    participants = Participant.objects.filter(event=event).order_by("id")
    
    #このイベントの持ち物
    items = (
        EventItem.objects
        .filter(event=event, is_selected=True)
        .select_related("bbq_item", "assignee")
        .order_by("id")
    )
    
    #進捗状況
    total_count = items.count()
    ready_count = items.filter(is_ready=True).count()
    progress_percent = int((ready_count / total_count) * 100 ) if total_count else 0
    
    if request.method == "POST":
        updated = []
        ready_item_ids = set(request.POST.getlist("ready_items"))
        
        for event_item in items:
            key = f"assignee_{event_item.id}"
            participant_id = request.POST.get(key)
            
            if participant_id:
                #このイベントの参加者かチェック
                assignee = participants.filter(id=participant_id).first()
            else:
                assignee = None
            
            new_is_ready = str(event_item.id) in ready_item_ids
            
            if (
                event_item.assignee_id != (assignee.id if assignee else None)
                or event_item.is_ready != new_is_ready
            ):
                event_item.assignee = assignee
                event_item.is_ready = new_is_ready
                updated.append(event_item)
                
        if updated:
            EventItem.objects.bulk_update(updated, ["assignee", "is_ready"])
            
        return redirect("item_assign", event_id=event.id)
        
    return render(
        request,
        "bbq_app/item_assign.html",
        {
            "event": event,
            "participants": participants,
            "items": items,
            "total_count": total_count,
            "ready_count": ready_count,
            "progress_percent": progress_percent,
        },
    )
    
#忘れ物登録
@login_required
def forgotten_item_create(request, event_id):
    event = get_object_or_404(Event, id=event_id, user=request.user)
    
    if request.method == "POST":
        form = ForgottenItemForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data["name"]
            category = form.cleaned_data["category"]
            
            BbqItem.objects.get_or_create(
                user=request.user,
                name=name,
                defaults={"category": category}
            )
    return redirect("item_edit", event_id=event.id)    
    
            

#イベント複製
@login_required
def event_duplicate(request, event_id):
    original_event = get_object_or_404(Event, id=event_id, user=request.user)
    
    new_event = Event.objects.create(
        user=request.user,
        name=f"{original_event.name} (複製)",
        held_at=original_event.held_at,
        location=original_event.location,
    )
    #元のEventItemを取得
    original_items = EventItem.objects.filter(event=original_event)
    #コピー
    EventItem.objects.bulk_create([
        EventItem(
            event=new_event,
            bbq_item=item.bbq_item,
            is_selected=item.is_selected,
            status=item.status,
        )
        for item in original_items
    ])
    return redirect("item_edit", event_id=new_event.id)

#全イベント一覧
@login_required
def event_list(request):
    status = request.GET.get("status", "upcoming")
    now = timezone.now()
    qs = Event.objects.filter(user=request.user)
    
    if status == "past":
        events = qs.filter(held_at__lt=now).order_by("-held_at")
    else:
        events = qs.filter(Q(held_at__gte=now) | Q(held_at__isnull=True)).order_by("held_at")
        
    return render(request, "bbq_app/event_list.html",{"events":events,"status":status,})

#イベント削除
@login_required
def event_delete(request, event_id):
    event = get_object_or_404(Event, id=event_id, user=request.user)
    
    if request.method =="POST":
        event.delete()
        return redirect("home")
    
    return render(request, "bbq_app/event_confirm_delete.html", {
        "event":event
    })
    
@login_required
def event_participants(request, event_id):
    event = get_object_or_404(Event, id=event_id, user=request.user)
    participants = Participant.objects.filter(event=event).order_by("id")
    
    if request.method == "POST":
        name = request.POST.get("name", "").strip()
        
        if name:
            Participant.objects.create(
                event=event,
                name=name
            )
            return redirect("event_participants", event_id=event.id)
    
    return render(request, "bbq_app/event_participants.html",{
        "event": event,
        "participants":participants,
    })          
 
#マイページ  
@never_cache        
@login_required
def mypage(request):
    return render(request, "bbq_app/mypage.html")

#ユーザー名変更
@login_required
def mypage_name(request):
    user = request.user
    
    if request.method == "POST":
        form = UserNameForm(request.POST)
        if form.is_valid():
            user.first_name = form.cleaned_data["name"]
            user.save()
            messages.success(request, 'ユーザー名を変更しました。')
            return redirect("mypage")
    else:
        form = UserNameForm(initial={"name": user.first_name})
        
    return render(request, "bbq_app/mypage_name.html", {"form": form, "user_obj": user })    

@login_required
def mypage_email(request):
    if request.method == "POST":
        form = EmailUpdateForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, "メールアドレスを変更しました。")
            return redirect("mypage")
        
    else:
        form = EmailUpdateForm()
        
    return render(request, "bbq_app/mypage_email.html", {"form": form, "current_email": request.user.email})
