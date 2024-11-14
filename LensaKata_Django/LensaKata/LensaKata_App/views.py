from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from .models import *

# Create your views here.
def home(request):
    reviews = ReviewCard.objects.all()
    return render(request, 'home/home.html', {'reviews': reviews})

def form_name_view(request):
    form = FormName()  # Notice: corrected without `forms.`
    return render(request, 'form_name.html', {'form': form})

def login(request):
    return render(request, 'login.html')

def mabar(request):
    return render(request, 'home/mabar.html')

def game(request):
    return render(request, 'home/game.html')

def subscribe(request):
    if request.method == 'POST':
        form = CustomerForm(request.POST)
        if form.is_valid():
            form.save()
            success_message = "Terima kasih telah berlangganan!"
            return render(request, 'subscribe.html', {'form': form, 'success_message': success_message})
    else:
        form = CustomerForm()

    return render(request, 'subscribe.html', {'form': form})