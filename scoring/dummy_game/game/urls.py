from django.urls import path
from .views import GameView, home

urlpatterns = [
    path('', home, name='home'),
    path('<int:pk>/', GameView.as_view(), name='game'),
]
