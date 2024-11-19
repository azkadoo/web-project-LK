from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from .models import Story, GameSession


def game_view(request):
    # Ambil cerita pertama (atau atur logika pengambilan cerita lain)
    story = Story.objects.first()
    if not story:
        return render(request, 'game_app/error.html', {'message': 'No story available.'})

    if request.method == 'POST':
        user_input = request.POST.get('user_input', '').strip()

        # Validasi input kosong
        if not user_input:
            return JsonResponse({'error': 'Input cannot be empty.'}, status=400)

        # Simpan session permainan
        GameSession.objects.create(story=story, user_input=user_input)
        return JsonResponse({'message': 'Your input has been recorded. Thank you!'})

    # Untuk GET, tampilkan cerita
    return render(request, 'game_app/game.html', {'story': story})
