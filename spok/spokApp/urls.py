from django.urls import path
from .views import user_login, dashboard, spok_game, spok_result

urlpatterns = [
    # path('login/', user_login, name='login'),
    path('', user_login, name='login'),
    path('dashboard/', dashboard, name='dashboard'),
    path('spok_game/', spok_game, name='spok_game'),
    path('spok_result/<int:session_id>/', spok_result, name='spok_result'),
]
