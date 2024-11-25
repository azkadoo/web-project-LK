from django.urls import path
from .views import GameView

urlpatterns = [
    path('<int:pk>/', GameView.as_view(), name='game'),
]
