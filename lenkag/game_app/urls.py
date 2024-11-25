from django.urls import path
from . import views

urlpatterns = [
    # Root URL aplikasi `game_app`
    path('', views.game_view, name='game_view'),
    # path('', views.index, name='index'),
]
