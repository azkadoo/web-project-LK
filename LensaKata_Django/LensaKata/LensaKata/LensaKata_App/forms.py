from django import forms
from .models import *


class GameChallengeForm(forms.ModelForm):
    class Meta:
        model = GameChallenge
        fields = ['content']

def get(dictionary, key):
    """Mengambil item dari dictionary berdasarkan key."""
    return dictionary.get(key)