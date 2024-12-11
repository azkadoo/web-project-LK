# mengarang/views.py

from django.shortcuts import render, redirect
from .models import GameChallenge
from .forms import GameChallengeForm


def game_view(request):
    """
    Halaman untuk menulis cerita.
    Jika form di-submit, cerita disimpan dan pengguna diarahkan ke halaman hasil.
    """
    if request.method == 'POST':
        form = GameChallengeForm(request.POST)
        if form.is_valid():
            # Menyimpan cerita yang ditulis oleh user
            game_challenge = form.save(commit=False)
            game_challenge.save()  # Menyimpan cerita tanpa user
            return redirect('game_result', pk=game_challenge.pk)  # Redirect ke hasil permainan
    else:
        form = GameChallengeForm()

    return render(request, 'mengarang/game.html', {'form': form})


def game_result_view(request, pk):
    """
    Halaman untuk menampilkan hasil cerita yang sudah ditulis beserta skor.
    """
    game_challenge = GameChallenge.objects.get(pk=pk)
    return render(request, 'mengarang/game_result.html', {'game_challenge': game_challenge})
