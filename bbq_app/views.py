from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.views import LoginView
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from .forms import SignupForm, EventForm
from .models import Event, BbqItem, EventItem
from django.utils import timezone
from django.db.models import Q
from datetime import datetime
from django.views.generic import CreateView, UpdateView

def combine_to_held_at(date, time):
    dt = datetime.combine(date, time)
    return timezone.make_aware(dt, timezone.get_default_timezone())

def portfolio(request):
    return render(request, 'bbq_app/portfolio.html')

#ホームにイベントを３つまで表示
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
            event.held_at = combine_to_held_at(form.cleaned_data["date"], form.cleaned_data["time"])
            event.save()
            
            #テンプレートをイベントにコピー
            templates = BbqItem.objects.filter(user=request.user)
            EventItem.objects.bulk_create([
                EventItem(event=event, bbq_item=t, status=1, is_selected=False)
                for t in templates
            ])
            
            return redirect("item_edit", event_id=event.id)
    else:
        form = EventForm()
        
    return render(request, "bbq_app/event_form.html", {"form":form})

#持ち物編集リスト①
@login_required
def item_edit(request, event_id):
    event = get_object_or_404(Event, id=event_id, user=request.user)
    items = EventItem.objects.filter(event=event).select_related("bbq_item")
    total_count = items.count()#持ち物進捗
    selected_count = items.filter(is_selected=True).count()
    
    if request.method == "POST":
        selected_ids = request.POST.getlist("selected_items")
        
        #全部一旦False
        EventItem.objects.filter(event=event).update(is_selected=False)
        
        #チェックされたものだけTrue
        EventItem.objects.filter(event=event, id__in=selected_ids).update(is_selected=True)
        
        return redirect("item_edit", event_id=event.id)
    
    if total_count > 0:
        progress_percent = int((selected_count / total_count) * 100)
    else:
        progress_percent = 0
    
    return render(request, "bbq_app/item_edit.html", {
        "event":event, 
        "items":items,
        "total_count":total_count,
        "selected_count":selected_count,
        "progress_percent":progress_percent,
    })

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

#全イベント詳細
@login_required
def event_list(request):
    events = Event.objects.filter(user=request.user).order_by("-held_at")
    return render(request, "bbq_app/event_list.html", {"events":events})

#イベント削除
@login_required
def event_delete(request, event_id):
    event = get_object_or_404(Event, id=event.id, user=request.user)
    
    if request.method =="POST":
        event.delete()
        return redirect("home")
    
    return render(request, "bbq_app/event_confirm_delete.html", {
        "event":event
    })
    
            
            