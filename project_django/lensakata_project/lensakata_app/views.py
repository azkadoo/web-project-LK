from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader

def index(request):
    template = loader.get_template('lensakata_app/index.html')
    return HttpResponse(template.render())

def game(request):
    template = loader.get_template('lensakata_app/game.html')
    return HttpResponse(template.render())

def pulau_kata(request):
    template = loader.get_template('lensakata_app/pulau_kata.html')
    return HttpResponse(template.render())

def sambung_kata(request):
    template = loader.get_template('lensakata_app/sambung_kata.html')
    return HttpResponse(template.render())
def sinonim_antonim(request):
    template = loader.get_template('lensakata_app/sinonim_antonim.html')
    return HttpResponse(template.render())

def login(request):
    return render(request,'lensakata_app/login.html')

def mabar(request):
    return render(request,'lensakata_app/mabar.html')