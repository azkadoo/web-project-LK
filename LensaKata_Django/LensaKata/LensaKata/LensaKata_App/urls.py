from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include
from LensaKata_App import views
from .views import *

urlpatterns = [
    path('google-one-tap-login/', google_one_tap_login, name='google_one_tap_login'),
    path('google-login/', google_login, name='google_login'),
    path('home/', views.home, name='home'), 
    path('promo-langganan/', views.langganan_home, name='langganan_home'), 
    path('mabar/', views.mabar, name='mabar'),    
    #path('game/', views.game, name='game'),
    path('dashboard/', views.dashboard, name='dashboard'), 
    path('langganan/', views.langganan, name='langganan'), 
    path('game/<int:pk>/', GameView.as_view(), name='game'),
    path('mengarang/', views.mengarang_view, name='mengarang'),
    path('mengarang/result/<int:pk>/', views.mengarang_result_view, name='mengarang_result'),
    path('accounts/', include('allauth.urls')),
    path('rate_game_challenge/<int:challenge_id>/', rate_game_challenge, name='rate_game_challenge'),
    path('game_challenge_dashboard/', game_challenge_dashboard, name='game_challenge_dashboard'),  # Pastikan ini ada
] 

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)