# mengarang/urls.py

from django.urls import path
from . import views

urlpatterns = [
    path('game/', views.game_view, name='game'),  # Halaman untuk menulis cerita
    path('game/result/<int:pk>/', views.game_result_view, name='game_result'),  # Halaman untuk melihat hasil
]
