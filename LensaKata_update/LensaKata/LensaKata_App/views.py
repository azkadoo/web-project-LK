from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.conf import settings
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages
from django.utils import timezone
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Sum
from django.db import transaction
from django.views import View
import requests
import json

from .models import Story, GameSession, UserProgress, ReviewCard
from .utils import get_user_level

# Create your views here.

@csrf_exempt
def google_one_tap_login(request):
    login_url = f"{settings.PUBLIC_DOMAIN_NAME}/accounts/google/login/"
    return HttpResponseRedirect(login_url)

@csrf_exempt  # Use with caution; consider using CSRF tokens for security
def google_login(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        id_token = data.get('credential')

        response = requests.get(f'https://oauth2.googleapis.com/tokeninfo?id_token={id_token}')
        if response.status_code == 200:
            user_info = response.json()
            email = user_info.get('email')

            user, created = User.objects.get_or_create(email=email)
            login(request, user)

            return JsonResponse({'status': 'success', 'url': '/'})
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
            return redirect('home')
    return render(request, 'login.html')

@login_required
def dashboard(request):
    stories = Story.objects.all()
    latest_game_session = GameSession.objects.filter(user=request.user).order_by('-created_at').first()
    total_score = GameSession.objects.filter(user=request.user).aggregate(Sum('score'))['score__sum'] or 0
    user_progress, created = UserProgress.objects.get_or_create(user=request.user)

    total_challenges_completed = user_progress.challenges_completed
    user_level = get_user_level(total_score)
    previous_level = user_progress.user_level if hasattr(user_progress, 'user_level') else 0

    if user_level > previous_level:
        user_progress.daily_score = 0
        user_progress.daily_words_learned = 0
        user_progress.daily_challenges_completed = 0

    level_thresholds = settings.LEVEL_THRESHOLDS
    next_level_score = level_thresholds[user_level - 1] if user_level <= len(level_thresholds) else None
    progress = (total_score / next_level_score) * 100 if next_level_score else 100

    all_matched_keywords = set()
    game_sessions = GameSession.objects.filter(user=request.user)
    for session in game_sessions:
        matched_keywords = session.matched_keywords.split(', ')
        all_matched_keywords.update(matched_keywords)

    latest_matched_keywords = []
    total_words_learned = len(all_matched_keywords)
    latest_score = latest_game_session.score if latest_game_session else 0
    latest_challenges_count = 1 if latest_game_session else 0
    latest_new_words_count = len(latest_matched_keywords) if latest_game_session else 0

    latest_matched_count = 0
    if latest_game_session:
        latest_matched_keywords = latest_game_session.matched_keywords.split(', ')
        latest_matched_count = len(latest_matched_keywords)

    return render(request, 'dashboard/dashboard.html', {
        'user': request.user,
        'stories': stories,
        'user_progress': user_progress,
        'latest_game_session': latest_game_session,
        'total_score': total_score,
        'total_challenges_completed': total_challenges_completed,
        'total_words_learned': total_words_learned,
        'latest_score': latest_score,
        'latest_challenges_count': latest_challenges_count,
        'latest_new_words_count': latest_new_words_count,
        'latest_matched_count': latest_matched_count,
        'user_level': user_level,
        'progress': progress,
    })

def home(request):
    reviews = ReviewCard.objects.all()
    return render(request, 'home/home.html', {'reviews': reviews})

@login_required
def mabar(request):
    return render(request, 'home/mabar.html')

class GameView(View):
    def get(self, request, pk):
        story = get_object_or_404(Story, pk=pk)
        return render(request, 'game/game.html', {'story': story})

    def post(self, request, pk):
        story = get_object_or_404(Story, pk=pk)
        
        # Ambil nilai dari input tags dan input text biasa
        user_answer_tags = request.POST.get('user_answer_tags', '').strip()
        user_answer_text = request.POST.get('user_answer', '').strip()
        
        # Gunakan tags jika ada, jika tidak gunakan text input
        user_answer = user_answer_tags if user_answer_tags else user_answer_text
        user_words = user_answer.split()
        
        # Ambil data dari field Story
        story_tags = [tag.strip() for tag in story.tags.split()] if story.tags else []
        story_answer = story.answer.strip() if story.answer else ""
        
        # Cek kecocokan kata dengan tags (case insensitive)
        matched_tags = [word for word in user_words if word.lower() in [tag.lower() for tag in story_tags]]
        
        # Cek kecocokan dengan jawaban yang benar (case insensitive)
        is_perfect_match = user_answer.lower() == story_answer.lower()

        # Cek urutan kata
        is_correct_order = False
        if len(user_words) == len(story_tags):
            is_correct_order = all(
                user_word.lower() == tag.lower()
                for user_word, tag in zip(user_words, story_tags)
            )

        # Hitung skor berdasarkan kecocokan
        if is_perfect_match:
            feedback = "Tersusun (highest): Jawaban sempurna!"
            score = 100
        elif is_correct_order:
            feedback = "Tersusun dengan baik: Kata kunci lengkap dan urutan benar!"
            score = 90
        elif len(matched_tags) == len(story_tags):
            feedback = "Tidak tersusun: Kata kunci lengkap, tapi kalimat belum tersusun dengan baik."
            score = 80
        elif matched_tags:
            percentage = len(matched_tags) / len(story_tags)
            score = int(60 * percentage)  # Skor proporsional berdasarkan persentase kecocokan
            feedback = f"Cukup: {len(matched_tags)} dari {len(story_tags)} kata kunci ditemukan"
        else:
            feedback = "Tidak cukup: Tidak ada kata kunci yang cocok."
            score = 0

        # Update progress
        user_progress, created = UserProgress.objects.get_or_create(user=request.user)
        user_progress.challenges_completed += 1
        user_progress.daily_score += score
        user_progress.daily_words_learned += len(matched_tags)
        user_progress.daily_challenges_completed += 1
        user_progress.save()

        # Simpan sesi
        GameSession.objects.create(
            user=request.user,
            score=score,
            matched_keywords=', '.join(matched_tags)
        )

        return render(request, 'game/result.html', {
            'story': story,
            'is_correct': is_perfect_match,
            'user_answer': user_answer,
            'feedback': feedback,
            'score': score,
            'matched_tags': matched_tags,
            'total_tags': len(story_tags),
            'correct_answer': story_answer
        })