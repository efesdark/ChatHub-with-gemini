from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

from django.contrib import messages
from .forms import RegisterForm
from .models import ChatMessage



from django.http import JsonResponse
import google.generativeai as genai
from django.conf import settings
from django.views.decorators.csrf import csrf_protect



# .env yükleme
from dotenv import load_dotenv
from pathlib import Path
import os
load_dotenv()
api_key0 = os.getenv('GOOGLE_API_KEY')
print(api_key0[:5]) #first 5 key of api

def home(request):
    return render(request, "home.html")


def sign_in(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect("profile")
        else:
            return render(request, "sign_in.html", {"error": "Invalid credentials"})
    return render(request, "sign_in.html")

def sign_up(request):
    if request.method == "POST":
        username = request.POST["username"]
        password1 = request.POST["password1"]
        password2 = request.POST["password2"]
        if password1 == password2:
            user = User.objects.create_user(username=username, password=password1)
            login(request, user)
            return redirect("profile")
        else:
            return render(request, "sign_up.html", {"error": "Passwords do not match"})
    return render(request, "sign_up.html")

def user_logout(request):
    logout(request)
    return redirect("home")

# Gemini konfigürasyonu



# chathubapp/views.py
"""
from django.conf import settings
from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth.decorators import login_required
import google.generativeai as genai
"""

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import ChatMessage
from .gemini_client import get_gemini_response

@login_required
def profile(request):
    if request.method == "POST":
        user_message = request.POST.get("message")
        if user_message:
            try:
                response = get_gemini_response(user_message)
                ChatMessage.objects.create(
                    user=request.user,
                    message=user_message,
                    response=response,
                )
            except Exception as e:
                response = f"Hata: {str(e)}"
    messages_list = ChatMessage.objects.filter(user=request.user).order_by("-timestamp")
    return render(request, "profile.html", {"messages": messages_list})






"""
@csrf_protect
@login_required
def profile(request):
    if request.method == 'POST':
        try:
            # API anahtarını settings'den direkt al
            genai.configure(
                api_key=settings.GOOGLE_API_KEY,
                client_options={
                    'api_endpoint': 'https://generativelanguage.googleapis.com/v1beta'
                }
            )
            
            model = genai.GenerativeModel('gemini-2.0-flash')
            user_message = request.POST.get('message', '')
            
            # Streaming olmadan normal response
            response = model.generate_content(user_message)
            
            return JsonResponse({
                'response': response.text,
                'status': 'success'
            })
            
        except Exception as e:
            return JsonResponse({
                'error': str(e),
                'status': 'error'
            }, status=500)
    
    # GET istekleri için
    return render(request, 'profile.html', {
        'user': request.user,
        'csrf_token': request.COOKIES.get('csrftoken', '')  # CSRF token'ı template'e gönder
    })

    """