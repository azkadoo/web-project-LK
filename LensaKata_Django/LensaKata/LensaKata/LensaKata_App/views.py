from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.conf import settings
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages
from django.utils import timezone
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Sum, Avg
from django.db import transaction
from django.views import View
from .forms import *
import requests
import json

from .models import *
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
    # Retrieve or create the user_progress instance first
    user_progress, created = UserProgress.objects.get_or_create(user=request.user)
    # Instead of incrementing, directly assign the count of completed challenges
    # Save the updated progress
    game_challenges = GameChallenge.objects.exclude(user=request.user)  # Ambil tantangan yang bukan milik pengguna saat ini
    
    leaderboard_data = User.objects.annotate(
        total_score=Sum('gamesession__score')
    ).filter(total_score__gt=0).order_by('-total_score')[:10]

    # Retrieve stories and latest game session
    stories = Story.objects.all()
    latest_game_challenge = GameChallenge.objects.filter(user=request.user).order_by('-created_at').first()
    latest_game_session = GameSession.objects.filter(user=request.user).order_by('-created_at').first()
    
    # Tentukan latest_score berdasarkan game yang lebih baru
    if latest_game_challenge and latest_game_session:
        latest_score = (
            latest_game_challenge.score
            if latest_game_challenge.created_at > latest_game_session.created_at
            else latest_game_session.score
        )
    elif latest_game_challenge:
        latest_score = latest_game_challenge.score
    elif latest_game_session:
        latest_score = latest_game_session.score
    else:
        latest_score = 0

    # Calculate total scores
    total_score = GameSession.objects.filter(user=request.user).aggregate(Sum('score'))['score__sum'] or 0
    total_mengarang_score = GameChallenge.objects.filter(user=request.user).aggregate(Sum('score'))['score__sum'] or 0

    # Update user progress
    user_progress.daily_score = total_score + total_mengarang_score  # Set daily_score to the total mengarang score
    user_progress.save()  # Save changes to user_progress

    # Determine user level
    user_level = get_user_level(total_score)
    previous_level = user_progress.user_level if hasattr(user_progress, 'user_level') else 0

    if user_level > previous_level:
        user_progress.daily_score = 0
        user_progress.daily_words_learned = 0
        user_progress.daily_challenges_completed = 0

    # Calculate progress
    level_thresholds = settings.LEVEL_THRESHOLDS
    next_level_score = level_thresholds[user_level - 1] if user_level <= len(level_thresholds) else None
    progress = (total_score / next_level_score) * 100 if next_level_score else 100

    # Collect matched keywords
    all_matched_keywords = set()
    game_sessions = GameSession.objects.filter(user=request.user)
    for session in game_sessions:
        matched_keywords = session.matched_keywords.split(', ')
        all_matched_keywords.update(matched_keywords)

    # Prepare data for rendering
    latest_matched_keywords = []
    total_words_learned = len(all_matched_keywords)
    
    # Ambil latest score dari GameChallenge
    latest_game_challenge = GameChallenge.objects.filter(user=request.user).order_by('-created_at').first()    
    latest_challenges_count = 1 if latest_game_session else 0
    latest_new_words_count = len(latest_matched_keywords) if latest_game_session else 0

    latest_matched_count = 0
    if latest_game_session:
        latest_matched_keywords = latest_game_session.matched_keywords.split(', ')
        latest_matched_count = len(latest_matched_keywords)

    return render(request, 'dashboard/dashboard.html', {
        'user': request.user,
        'stories': stories,
        'leaderboard_data': leaderboard_data,
        'user_progress': user_progress,
        'latest_game_session': latest_game_session,
        'game_challenges': game_challenges,
        'total_score': total_score + total_mengarang_score,  # Total skor
        'total_challenges_completed': user_progress.challenges_completed,
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

def langganan_home(request):
    paket_list = Paketlangganan.objects.order_by('id')
    paket_dict = {'tampil': paket_list}
    return render(request, 'home/langganan_home.html', context=paket_dict)

@login_required
def mabar(request):
    return render(request, 'home/mabar.html')

@login_required
def langganan(request):
    paket_list = Paketlangganan.objects.order_by('id')
    paket_dict = {'tampil':paket_list}
    return render(request,'dashboard/langganan.html', context=paket_dict)

class GameView(View):
    def get(self, request, pk):
        story = get_object_or_404(Story, pk=pk)
        return render(request, 'game/game.html', {'story': story})

    def post(self, request, pk):
        story = get_object_or_404(Story, pk=pk)
        user_answer = request.POST.get('user_answer', '').strip()
        user_words = user_answer.split()
        keywords = story.get_keywords()
        correct_sentences = story.get_answers()
        correct_answer = ' '.join(correct_sentences)
        next_story = Story.objects.filter(id__gt=pk).order_by('id').first()  # Mengambil cerita dengan id lebih besar dari pk saat ini

        matched_keywords = [word for word in user_words if word in keywords]
        keyword_index = 0
        for word in user_words:
            if word.lower() == keywords[keyword_index].lower():
                keyword_index += 1
            if keyword_index == len(keywords):
                break

        if user_answer.strip() == correct_answer:
            feedback = "Tersusun (highest): Jawaban sempurna!"
            score = 100
        elif matched_keywords == keywords:
            feedback = "Tidak tersusun: Kata kunci lengkap, tapi kalimat belum tersusun dengan baik."
            score = 80
        elif len(matched_keywords) > 0:
            feedback = f"Cukup: {len(matched_keywords)} kata kunci ditemukan"
            score = 50
        else:
            feedback = "Tidak cukup: Tidak ada kata kunci yang cocok."
            score = 0

        user_progress, created = UserProgress.objects.get_or_create(user=request.user)
        user_progress.challenges_completed += 1
        user_progress.daily_score += score
        user_progress.daily_words_learned += len(matched_keywords)
        user_progress.daily_challenges_completed += 1
        user_progress.save()

        GameSession.objects.create(
            user=request.user,
            score=score,
            matched_keywords=', '.join(matched_keywords)
        )

        return render(request, 'game/result.html', {
            'story': story,
            'user_answer': user_answer,
            'feedback': feedback,
            'score': score,
            'next_story': next_story
        })

def mengarang_view(request):
    """
    Halaman untuk menulis cerita.
    Jika form di-submit, cerita disimpan dan pengguna diarahkan ke halaman hasil.
    """
    if request.method == 'POST':
        form = GameChallengeForm(request.POST)
        if form.is_valid():
            # Menyimpan cerita yang ditulis oleh user
            game_challenge = form.save(commit=False)
            game_challenge.user = request.user  # Set user
            game_challenge.save()  # Simpan cerita
            
            # Update user_progress dengan skor game mengarang
            user_progress, created = UserProgress.objects.get_or_create(user=request.user)
            user_progress.daily_score += game_challenge.score  # Menambahkan skor game mengarang
            user_progress.daily_challenges_completed += 1
            user_progress.save()  # Simpan perubahan

            return redirect('mengarang_result', pk=game_challenge.pk)  # Redirect ke hasil permainan
    else:
        form = GameChallengeForm()

    return render(request, 'mengarang/game.html', {'form': form})


def mengarang_result_view(request, pk):
    """
    Halaman untuk menampilkan hasil cerita yang sudah ditulis beserta skor.
    """
    game_challenge = GameChallenge.objects.get(pk=pk)
    return render(request, 'mengarang/result.html', {'game_challenge': game_challenge})

def leaderboard(request):
    leaderboard_data = User.objects.annotate(
        total_score=Sum('gamesession__score')
    ).filter(total_score__gt=0).order_by('-total_score')[:10]

    # Ambil rata-rata rating untuk setiap GameChallenge
    game_challenge_ratings = GameChallenge.objects.annotate(
        average_rating=Avg('storyrating__rating')
    ).order_by('-average_rating')[:10]  # Ambil 10 tantangan teratas berdasarkan rating

    return render(request, 'dashboard/leaderboard.html', {
        'leaderboard_data': leaderboard_data,
        'game_challenge_ratings': game_challenge_ratings,
    })

@login_required
def game_challenge_dashboard(request):
    # Ambil semua GameChallenge yang dibuat oleh pengguna lain
    game_challenges = GameChallenge.objects.exclude(user=request.user)  # Ambil tantangan yang bukan milik pengguna saat ini

    # Ambil rating untuk setiap GameChallenge
    game_challenge_ratings = {
        challenge.id: StoryRating.objects.filter(game_challenge=challenge).aggregate(average_rating=Avg('rating'))['average_rating']
        for challenge in game_challenges
    }

    return render(request, 'dashboard/dashboard.html', {
        'game_challenges': game_challenges,
        'game_challenge_ratings': game_challenge_ratings,
    })

@login_required
def rate_game_challenge(request, challenge_id):
    if request.method == 'POST':
        rating_value = request.POST.get('rating')
        game_challenge = get_object_or_404(GameChallenge, id=challenge_id)

        # Simpan rating
        StoryRating.objects.update_or_create(
            user=request.user,
            game_challenge=game_challenge,
            defaults={'rating': rating_value}
        )

        return redirect('game_challenge_dashboard')  # Redirect ke halaman dashboard tantangan
