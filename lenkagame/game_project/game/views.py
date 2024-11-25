from django.shortcuts import render
from django.views import View
from .models import Story


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
