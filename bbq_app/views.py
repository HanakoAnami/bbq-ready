from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.views import LoginView
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from .forms import SignupForm, EventForm
from .models import Event, BbqItem, EventItem

def portfolio(request):
    return render(request, 'bbq_app/portfolio.html')

@login_required
def home(request):
    events = Event.objects.filter(user=request.user).order_by("date")[3:]
    return render(request, 'bbq_app/home.html', {"events": events})

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

@login_required
def event_create(request):
    if request.method =="POST":
        form = EventForm(request.POST)
        if form.is_valid():
            event = form.save(commit=False)
            event.user = request.user
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

@login_required
#持ち物編集リスト①
def item_edit(request, event_id):
    event = get_object_or_404(Event, id=event_id, user=request.user)
    items = EventItem.objects.filter(event=event).select_related("bbq_item")
    
    return render(request, "bbq_app/item_edit.html", {"event":event, "items":items})


            
            