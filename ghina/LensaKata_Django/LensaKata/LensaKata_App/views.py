from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from .models import *

# Create your views here.
def home(request):
    reviews = ReviewCard.objects.all()
    return render(request, 'home.html', {'reviews': reviews})

def form_name_view(request):
    form = FormName()  # Notice: corrected without `forms.`
    return render(request, 'form_name.html', {'form': form})

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
