# mengarang/forms.py

from django import forms
from .models import GameChallenge


class GameChallengeForm(forms.ModelForm):
    class Meta:
        model = GameChallenge
        fields = ['content']
