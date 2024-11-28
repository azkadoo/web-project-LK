from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages
from myauth.forms import LoginForm
from django.template import loader
from django.http import HttpResponse

# Create your views here.

def login_view(request):
    form = LoginForm()
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request,user)
                return redirect('home')  # Ganti 'home' dengan nama URL halaman home Anda
            else:
                messages.error(request, "Username atau password salah")
        else:
            form = LoginForm()
    return render(request, 'lensakata_app/loginn.html', {'form': form})

def home(request):
    return render(request, 'lensakata_app/home.html')

def login(request):
    template = loader.get_template('lensakata_app/login.html')
    return HttpResponse(template.render())