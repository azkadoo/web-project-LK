"""
URL configuration for lensakata_project project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from lensakata_app import views
from django.urls.conf import include

urlpatterns =[
    path('', views.index, name='index'),
    path('admin/', admin.site.urls),
    path('lensakata_app/', include('lensakata_app.urls')),
    path('game/', views.game, name='game'),
    path('pulau_kata/', views.pulau_kata, name='pulau_kata'),
    path('sambung_kata/', views.sambung_kata, name='sambung_kata'),
    path('sinonim_antonim/', views.sinonim_antonim, name='sinonim_antonim'),
    path('mabar/', views.mabar, name='mabar'),
    path('tentangkami/', views.tentangkami, name='tentangkami'),
    path('', include('myauth.urls')),
    path('accounts/', include('allauth.urls')),
    path('startgame/', views.startgame, name='startgame'),
]
