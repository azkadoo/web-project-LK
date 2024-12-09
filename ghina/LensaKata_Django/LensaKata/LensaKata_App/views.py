from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.conf import settings
from django.template import loader
from .models import *
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages
from django.views import View
from django.utils import timezone
from django.contrib.auth.mixins import LoginRequiredMixin
import requests
from django.contrib.auth import login
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User

# Create your views here.

@csrf_exempt
def google_one_tap_login(request):
    # Construct the login URL for Google
    login_url = f"{settings.PUBLIC_DOMAIN_NAME}/accounts/google/login/"
    # Redirect the user to the Google login URL
    return HttpResponseRedirect(login_url)

@csrf_exempt  # Use with caution; consider using CSRF tokens for security
def google_login(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        id_token = data.get('credential')

        # Verify the ID token with Google
        response = requests.get(f'https://oauth2.googleapis.com/tokeninfo?id_token={id_token}')
        if response.status_code == 200:
            user_info = response.json()
            email = user_info.get('email')

            # Here you can create a new user or log in an existing user
            user, created = User.objects.get_or_create(email=email)
            login(request, user)  # Log the user in

            return JsonResponse({'status': 'success', 'url': '/'})  # Redirect URL after login
        else:
            return JsonResponse({'status': 'error', 'message': 'Invalid token'}, status=400)

    return JsonResponse({'status': 'error', 'message': 'Invalid request'}, status=400)

@login_required
def profile(request):
    return render(request, 'profile.html')

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')  # Redirect to home or another page after login
    return render(request, 'login.html')  # Render the login page if GET request

@login_required

def dashboard(request):
    return render(request, 'dashboard/dashboard.html', {'user': request.user})

def home(request):
    reviews = ReviewCard.objects.all()
    return render(request, 'home/home.html', {'reviews': reviews})

@login_required
def mabar(request):
    return render(request, 'home/mabar.html')

class GameView(LoginRequiredMixin, View):
    login_url = '/accounts/login/'  # Redirect to this URL if not logged in

    def get(self, request, pk):
        story = get_object_or_404(Story, pk=pk)
        return render(request, 'game/game.html', {'story': story, 'user': request.user})

    def post(self, request, pk):
        story = get_object_or_404(Story, pk=pk)
        user_answer = request.POST.get('user_answer', '').lower()
        valid_answers = [ans.lower() for ans in story.get_answers()]
        is_correct = any(ans in user_answer for ans in valid_answers)
        return render(request, 'game/result.html', {'story': story, 'is_correct': is_correct, 'user': request.user})

class GameView2(LoginRequiredMixin, View):
    login_url = '/accounts/login/'  # Redirect to this URL if not logged in

    def get(self, request, pk):
        story = get_object_or_404(Story, pk=pk)
        return render(request, 'game_home/game.html', {'story': story, 'user': request.user})

    def post(self, request, pk):
        story = get_object_or_404(Story, pk=pk)
        user_answer = request.POST.get('user_answer', '').lower()
        valid_answers = [ans.lower() for ans in story.get_answers()]
        is_correct = any(ans in user_answer for ans in valid_answers)
        return render(request, 'game_home/result.html', {'story': story, 'is_correct': is_correct, 'user': request.user})
