from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include
from LensaKata_App import views
from .views import *

urlpatterns = [
    path('google-one-tap-login/', google_one_tap_login, name='google_one_tap_login'),
    path('google-login/', google_login, name='google_login'),
    path('home/', views.home, name='home'), 
    path('mabar/', views.mabar, name='mabar'),    
    #path('game/', views.game, name='game'),
    path('dashboard/', views.dashboard, name='dashboard'), 
    path('game/<int:pk>/', GameView.as_view(), name='game'),
    path('accounts/', include('allauth.urls')),
    path('subscription/', views.subscription_page, name="subscription"),
    # Endpoint untuk menangani konfirmasi pembayaran dari Midtrans
    path('payment-success/', views.payment_success, name="payment_success"),
    # Halaman kursus dan mentoring, hanya bisa diakses jika langganan aktif
    path('course/', views.course_mentoring_page, name="course_mentoring_page"),
] 

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)