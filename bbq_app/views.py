from django.shortcuts import render, redirect
from django.contrib.auth.views import LoginView
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from .forms import SignupForm, EventForm

def portfolio(request):
    return render(request, 'bbq_app/portfolio.html')

@login_required
def home(request):# ログイン後の画面用
    return render(request, 'bbq_app/home.html')

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
    if request.method == "POST":
        form = EventForm(request.POST)
        if form.is_valid():
            event = form.save(commit=False)
            event.user = request.user
            event.save()
            return redirect("home")
        
    else:
        form = EventForm()
        
    return render(request,"bbq_app/event_form.html", {"form": form})
            
            