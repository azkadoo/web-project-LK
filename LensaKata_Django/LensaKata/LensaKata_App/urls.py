from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include
from . import views
from django.contrib.auth import views as auth_views
from .views import GameView

urlpatterns = [
    path('home/', views.home, name='home'),  # URL path is now 'home/'
    path('mabar/', views.mabar, name='mabar'),    
    #path('game/', views.game, name='game'),
    path('game/<int:pk>/', GameView.as_view(), name='game'),
    path('accounts/login', views.login, name='login'),
    path('accounts/signup/', views.login, name='signup'),
    path('accounts/logout/', auth_views.LogoutView.as_view(), name='logout'),
] 

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)