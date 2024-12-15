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
from .services.midtrans_service import create_payment_transaction
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
from .models import *
from django.db import connection
from django.contrib.auth.mixins import LoginRequiredMixin
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

@login_required
def dashboard(request):
    # Retrieve or create the user_progress instance first
    user_progress, created = UserProgress.objects.get_or_create(user=request.user)
    
    latest_scores = GameSession.objects.filter(user=OuterRef('pk')).order_by('-created_at').values('score')[:1]
    all_users = User.objects.annotate(
        total_score=Sum('gamesession__score') + Sum('gamechallenge__score'),
        latest_score=Subquery(latest_scores)  # Ambil score dari sesi terakhir
    )
    # Instead of incrementing, directly assign the count of completed challenges
    # Save the updated progress
    game_challenges = GameChallenge.objects.exclude(user=request.user)  # Ambil tantangan yang bukan milik pengguna saat ini
    
    user_sessions = SPOKSession.objects.filter(user=request.user).order_by('-created_at')

    # Retrieve stories and latest game session
    stories = Story.objects.all()
    latest_game_challenge = GameChallenge.objects.filter(user=request.user).order_by('-created_at').first()
    latest_game_session = GameSession.objects.filter(user=request.user).order_by('-created_at').first()
    latest_spok_session = SPOKSession.objects.filter(user=request.user).order_by('-created_at').first()

    latest_score = 0  # Default value

    # Tentukan latest_score berdasarkan game yang lebih baru
    if latest_game_challenge or latest_game_session or latest_spok_session:
        if latest_game_challenge and (not latest_game_session or latest_game_challenge.created_at > latest_game_session.created_at) and (not latest_spok_session or latest_game_challenge.created_at > latest_spok_session.created_at):
            latest_score = latest_game_challenge.score
        elif latest_game_session and (not latest_game_challenge or latest_game_session.created_at > latest_game_challenge.created_at) and (not latest_spok_session or latest_game_session.created_at > latest_spok_session.created_at):
            latest_score = latest_game_session.score
        elif latest_spok_session and (not latest_game_challenge or latest_spok_session.created_at > latest_game_challenge.created_at) and (not latest_game_session or latest_spok_session.created_at > latest_game_session.created_at):
            latest_score = latest_spok_session.score

    # Update latest_challenges_count
    user_progress.latest_challenges_count = user_progress.challenges_completed
    user_progress.save()

    # Calculate total scores
    total_score = GameSession.objects.filter(user=request.user).aggregate(Sum('score'))['score__sum'] or 0
    total_mengarang_score = GameChallenge.objects.filter(user=request.user).aggregate(Sum('score'))['score__sum'] or 0
    total_spok_score = SPOKSession.objects.filter(user=request.user).aggregate(Sum('score'))['score__sum'] or 0

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

    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT u.id, u.username,
                COALESCE(gs.total_score, 0) + COALESCE(gc.total_score, 0) + COALESCE(sp.total_score, 0) AS total_score
            FROM auth_user u
            LEFT JOIN (
                SELECT user_id, SUM(score) AS total_score
                FROM LensaKata_App_gamesession
                GROUP BY user_id
            ) gs ON u.id = gs.user_id
            LEFT JOIN (
                SELECT user_id, SUM(score) AS total_score
                FROM LensaKata_App_gamechallenge
                GROUP BY user_id
            ) gc ON u.id = gc.user_id
            LEFT JOIN (
                SELECT user_id, SUM(score) AS total_score
                FROM LensaKata_App_spoksession
                GROUP BY user_id
            ) sp ON u.id = sp.user_id
            GROUP BY u.id, u.username
            HAVING COALESCE(gs.total_score, 0) + COALESCE(gc.total_score, 0) + COALESCE(sp.total_score, 0) > 0
            ORDER BY total_score DESC
            LIMIT 10;
        """)
        leaderboard = cursor.fetchall()  # Ini akan menjadi list of tuples
        
    return render(request, 'dashboard/dashboard.html', {
        'user': request.user,
        'stories': stories,
        'user_progress': user_progress,
        'latest_game_session': latest_game_session,
        'game_challenges': game_challenges,
        'total_score': total_score + total_mengarang_score + total_spok_score,  # Total skor
        'total_challenges_completed': user_progress.challenges_completed,
        'total_words_learned': total_words_learned,
        'latest_score': latest_score,
        'latest_spok_session': latest_spok_session,
        'latest_challenges_count': latest_challenges_count,
        'latest_new_words_count': latest_new_words_count,
        'latest_matched_count': latest_matched_count,
        'user_level': user_level,
        'progress': progress,
        'sessions': user_sessions,
        'leaderboard': leaderboard,
    })

def home(request):
    reviews = ReviewCard.objects.all()
    return render(request, 'home/home.html', {'reviews': reviews})

def tentang_kami(request):
    return render(request, 'home/tentangkami.html')

@login_required
def langganan_(request):
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

@login_required
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
            user_progress.challenges_completed += 1
            user_progress.daily_challenges_completed += 1
            user_progress.save()  # Simpan perubahan

            return redirect('mengarang_result', pk=game_challenge.pk)  # Redirect ke hasil permainan
    else:
        form = GameChallengeForm()

    return render(request, 'mengarang/game.html', {'form': form})

@login_required
def mengarang_result_view(request, pk):
    """
    Halaman untuk menampilkan hasil cerita yang sudah ditulis beserta skor.
    """
    game_challenge = GameChallenge.objects.get(pk=pk)
    return render(request, 'mengarang/result.html', {'game_challenge': game_challenge})

from django.db.models import Sum, OuterRef, Subquery

@login_required
def spok_game(request):
    # Check if a challenge is already stored in the session
    if 'current_challenge_id' not in request.session:
        # Fetch a random challenge
        challenge = SPOKChallenge.objects.order_by('?').first()  # Get a random challenge
        request.session['current_challenge_id'] = challenge.id  # Store the challenge ID in the session
    else:
        # Retrieve the challenge from the session
        challenge_id = request.session['current_challenge_id']
        challenge = SPOKChallenge.objects.get(id=challenge_id)

    form = SPOKForm()

    if request.method == "POST":
        form = SPOKForm(request.POST)
        if form.is_valid():
            answers = {
                'subject': form.cleaned_data['subject'],
                'predicate': form.cleaned_data['predicate'],
                'object': form.cleaned_data['object'],
                'description': form.cleaned_data.get('description', '')
            }
            correct_answers = {
                'subject': challenge.subject,
                'predicate': challenge.predicate,
                'object': challenge.object,
                'description': challenge.description
            }

            # Calculate score
            score = 0
            for key in answers:
                print(f"Checking {key}: User answer = {answers[key]}, Correct answer = {correct_answers[key]}")
                if answers[key].lower() == correct_answers[key].lower():
                    score += 5
                    print(f"Correct! Score is now: {score}")
                else:
                    print("Incorrect answer.")

            # Simpan sesi permainan
            session = SPOKSession.objects.create(
                user=request.user,
                challenge=challenge,
                score=score
            )

            # Update UserProgress
            user_progress, created = UserProgress.objects.get_or_create(user=request.user)
            user_progress.daily_score += score  # Tambahkan skor ke daily_score
            user_progress.challenges_completed += 1  # Tambahkan 1 ke total challenges completed
            user_progress.daily_challenges_completed += 1  # Tambahkan 1 ke daily challenges completed
            user_progress.save()  # Simpan perubahan

            return redirect('spok_result', session_id=session.id)

    return render(request, 'spok/spok_game.html', {
        'challenge': challenge,
        'form': form
    })

@login_required
def spok_result(request, session_id):
    session = get_object_or_404(SPOKSession, id=session_id)
    return render(request, 'spok/spok_result.html', {
        'session': session
    })

def subscription_page(request):
    """
    Halaman untuk memilih paket langganan dan memulai transaksi pembayaran.
    """
    if request.method == "POST":
        try:
            # Validasi apakah user sudah login
            if not request.user.is_authenticated:
                return JsonResponse({"error": "Anda harus login untuk melanjutkan."}, status=403)

            # Ambil jumlah bulan yang dipilih dari form
            months = int(request.POST.get('months'))
            if months not in [1,2, 3, 6, 12]:
                return JsonResponse({"error": "Durasi langganan tidak valid."}, status=400)

            # Hitung total pembayaran berdasarkan jumlah bulan
            amount = months * 100000  # 100.000 per bulan

            # Buat ID unik untuk transaksi
            order_id = f"{request.user.username}-{months}"
            redirect_url = create_payment_transaction(order_id, amount)

            # Simpan informasi transaksi sementara sebelum pembayaran selesai
            subscription, _ = Subscription.objects.get_or_create(user=request.user)
            subscription.is_active = False  # Belum aktif sampai pembayaran dikonfirmasi
            subscription.start_date = None  # Reset jika sebelumnya ada
            subscription.end_date = None
            subscription.save()

            # Berikan URL redirect untuk pembayaran
            if redirect_url:
                # Redirect langsung ke URL pembayaran
                return HttpResponseRedirect(redirect_url)
            else:
                return JsonResponse({"error": "Transaksi gagal dibuat"})

        except ValueError:
            return JsonResponse({"error": "Durasi langganan harus berupa angka yang valid."}, status=400)
        except Exception as e:
            return JsonResponse({"error": f"Terjadi kesalahan: {str(e)}"}, status=500)

    return render(request, 'dashboard/subscription.html')


def check_subscription(user):
    """
    Cek apakah pengguna memiliki langganan aktif dan valid.
    """
    if not user.is_authenticated:
        return False

    try:
        subscription = Subscription.objects.get(user=user)
        return subscription.is_subscription_valid()
    except Subscription.DoesNotExist:
        # Jika tidak ada langganan, return False
        return False

@login_required
def check_subscription_status(request):
    """
    Endpoint untuk mengecek status langganan aktif pengguna.
    Mengembalikan JSON untuk digunakan di frontend.
    """
    if check_subscription(request.user):
        return JsonResponse({"status": "active"})
    else:
        return JsonResponse({"status": "inactive"})

@login_required
def langganan(request):
    return render(request, 'dashboard/langganan.html')

def kursus(request):
    if not check_subscription(request.user):
        # Redirect ke halaman langganan jika langganan tidak aktif
        return redirect('/langganan')
    # Render halaman kursus jika langganan valid
    return render(request, 'course/kursus.html')

def kursus_list(request):
    if not check_subscription(request.user):
    # Redirect ke halaman langganan jika langganan tidak aktif
        return redirect('/langganan')
    
    kursus_list = Kursus.objects.all()  # Ambil semua kursus
    return render(request, 'course/kursus.html', {'kursus_list': kursus_list})

def mentoring(request):
    if not check_subscription(request.user):
        # Redirect ke halaman langganan jika langganan tidak aktif
        return redirect('/langganan')
    return render(request,'dashboard/mentoring.html')

def video_detail(request, kursus_id):
    # Mengambil kursus berdasarkan ID
    kursus = get_object_or_404(Kursus, id=kursus_id)
    # Ambil video detail yang terkait dengan kursus
    video_details = VideoDetail.objects.filter(kursus=kursus)
    
    return render(request, 'course/video_detail.html', {'kursus': kursus, 'video_details': video_details})

@login_required
def course_mentoring_page(request):
    """
    Halaman kursus dan mentoring.
    Hanya dapat diakses jika langganan aktif.
    """
    if not check_subscription(request.user):
        # Redirect ke halaman langganan jika langganan tidak aktif
        return redirect('/subscription')

    # Render halaman kursus jika langganan valid
    return render(request, 'course/mentoring.html')

from datetime import datetime
from dateutil.relativedelta import relativedelta  # Jika Anda memiliki error terkait ini, pastikan `python-dateutil` sudah terinstal.

@csrf_exempt
def payment_success(request):
    """
    Endpoint untuk menerima konfirmasi dari Midtrans.
    """
    if request.method == "GET":
        data = request.GET
    elif request.method == "POST":
        data = request.POST
    else:
        return JsonResponse({"error": "Invalid request method."})

    try:
        print("Request method:", request.method)
        print("Data dari Midtrans:", data.dict())

        # Periksa status pembayaran
        if data.get('status_code') == "200" and data.get('transaction_status') == "settlement":
            # Ambil order_id
            order_id = data.get('order_id')
            if not order_id:
                return JsonResponse({"error": "Order ID tidak ditemukan."})

            try:
                # Pecah order_id untuk mendapatkan username dan months
                username, months = order_id.split('-')
                months = int(months)  # Konversi ke integer
            except ValueError:
                return JsonResponse({"error": "Format Order ID tidak valid."})

            # Ambil pengguna berdasarkan username
            try:
                user = User.objects.get(username=username)
            except User.DoesNotExist:
                return JsonResponse({"error": "Pengguna tidak ditemukan."})

            # Hitung jumlah pembayaran (gross_amount)
            gross_amount = months * 100000  # 100.000 per bulan
            if gross_amount <= 0:
                return JsonResponse({"error": "Jumlah pembayaran tidak valid."})

            # Aktivasi langganan pengguna
            activate_user_subscription(user, months)

            # Kirim respons sukses
            
            return redirect('/langganan?payment_success=true')
        else:
            return JsonResponse({"error": "Konfirmasi pembayaran gagal."})

    except Exception as e:
        print("Kesalahan saat memproses notifikasi Midtrans:", str(e))
        return JsonResponse({"error": f"Kesalahan internal: {str(e)}"})


def activate_user_subscription(user, months):
    """
    Aktifkan langganan setelah pembayaran berhasil.
    """
    try:
        # Periksa apakah subscription sudah ada
        subscription, created = Subscription.objects.get_or_create(user=user)

        # Perbarui informasi aktifasi langganan
        subscription.is_active = True
        subscription.start_date = timezone.now()
        subscription.end_date = timezone.now() + timezone.timedelta(days=30 * months)
        subscription.save()

        print(f"Langganan berhasil diaktifkan untuk user: {user.username}")
        print("Detail langganan disimpan: ", subscription)
    except Exception as e:
        print("Kesalahan saat mengaktifkan langganan: ", e)