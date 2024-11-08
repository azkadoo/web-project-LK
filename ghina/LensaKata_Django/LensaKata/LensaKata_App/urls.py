from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from . import views

urlpatterns = [
    path('home/', views.home, name='home'),
    path('form/', views.form_name_view, name='form'),
    path('subscribe/', views.subscribe, name='subscribe')
] 

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)