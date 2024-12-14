from django import forms
from .models import SPOKChallenge


class SPOKForm(forms.Form):
    subject = forms.CharField(label="Subjek", widget=forms.TextInput(attrs={'class': 'form-control'}))
    predicate = forms.CharField(label="Predikat", widget=forms.TextInput(attrs={'class': 'form-control'}))
    object = forms.CharField(label="Objek", widget=forms.TextInput(attrs={'class': 'form-control'}))
    description = forms.CharField(label="Keterangan", required=False, widget=forms.TextInput(attrs={'class': 'form-control'}))
