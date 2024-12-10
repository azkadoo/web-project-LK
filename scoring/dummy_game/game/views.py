from django.shortcuts import render, get_object_or_404
from django.views import View
from .models import Story


def home(request):
    stories = Story.objects.all()  # Ambil semua cerita dari database
    return render(request, 'game/home.html', {'stories': stories})


class GameView(View):
    def get(self, request, pk):
        story = get_object_or_404(Story, pk=pk)
        return render(request, 'game/game.html', {'story': story})

    def post(self, request, pk):
        story = get_object_or_404(Story, pk=pk)
        user_answer = request.POST.get('user_answer', '').lower().strip()
        user_words = user_answer.split()  # Pecah jawaban user menjadi daftar kata
        keywords = story.get_keywords()  # Mengambil kata kunci dari tags
        correct_sentences = story.get_answers()  # Susunan kalimat yang benar

        # Analisis jawaban
        matched_keywords = [word for word in user_words if word in keywords]

        # Penilaian
        if matched_keywords == keywords and user_answer in correct_sentences:
            feedback = "Tersusun (highest): Jawaban sempurna!"
            score = 100
        elif matched_keywords == keywords:
            feedback = "Tidak tersusun: Kata kunci lengkap, tapi kalimat belum tersusun dengan baik."
            score = 80
        elif len(matched_keywords) > 0:
            feedback = f"Cukup: {len(matched_keywords)} kata kunci ditemukan"
            # dari len(keywords)} kata kunci ditemukan."
            score = 50
        else:
            feedback = "Tidak cukup: Tidak ada kata kunci yang cocok."
            score = 0

        return render(request, 'game/result.html', {
            'story': story,
            'user_answer': user_answer,
            'feedback': feedback,
            'score': score,
        })
