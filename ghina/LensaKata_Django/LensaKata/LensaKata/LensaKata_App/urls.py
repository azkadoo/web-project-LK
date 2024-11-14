from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from . import views

urlpatterns = [
    path('home/', views.home, name='home'),  # URL path is now 'home/'
    path('form/', views.form_name_view, name='form'),  # New path for the same view
    path('home/mabar/', views.mabar, name='mabar'),    
    path('home/game/', views.game, name='game'),
    path('subscribe/', views.subscribe, name='subscribe'),
    path('login/', views.login, name='login')
] 

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)