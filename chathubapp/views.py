from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import RegisterForm
from .chatbot import generate_gemini_response
from .models import ChatMessage

def home(request):
    return render(request, "home.html")

def sign_up(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('sign_in')
    else:
        form = RegisterForm()
    return render(request, 'sign_up.html', {'form': form})

def sign_in(request):
    if request.method == 'POST':
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect('profile')
        messages.error(request, 'Hatalı giriş')
    return render(request, 'sign_in.html')

def user_logout(request):
    logout(request)
    return redirect('home')

@login_required
def profile(request):
    if request.method == 'POST':
        user_message = request.POST.get("message")
        response = generate_gemini_response(user_message)
        ChatMessage.objects.create(user=request.user, message=user_message, response=response)
    messages_list = ChatMessage.objects.filter(user=request.user).order_by('-timestamp')
    return render(request, 'profile.html', {'messages': messages_list})
