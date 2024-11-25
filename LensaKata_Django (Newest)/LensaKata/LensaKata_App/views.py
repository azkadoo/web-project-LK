from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.template import loader
from .models import *
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.views import View

# Create your views here.

def home(request):
    reviews = ReviewCard.objects.all()
    return render(request, 'home/home.html', {'reviews': reviews})

def login(request):
    return render(request, 'account/login')

def signup(request):
    return render(request, 'account/signup')

def mabar(request):
    return render(request, 'home/mabar.html')

#def game(request):
    return render(request, 'home/game.html')

class GameView(View):
    def get(self, request, pk):
        story = Story.objects.get(pk=pk)
        return render(request, 'game/game.html', {'story': story})

    def post(self, request, pk):
        story = Story.objects.get(pk=pk)
        user_answer = request.POST.get('user_answer', '').lower()
        valid_answers = [ans.lower() for ans in story.get_answers()]
        is_correct = any(ans in user_answer for ans in valid_answers)
        return render(request, 'game/result.html', {'story': story, 'is_correct': is_correct})