from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include
from LensaKata_App import views
from .views import *

urlpatterns = [
    path('google-one-tap-login/', google_one_tap_login, name='google_one_tap_login'),
    path('google-login/', google_login, name='google_login'),
    path('home/', views.home, name='home'), 
    path('subscription/', views.subscription_page, name="subscription"),
    # Endpoint untuk menangani konfirmasi pembayaran dari Midtrans 
    path('payment-success/', views.payment_success, name="payment_success"),
    # Halaman kursus dan mentoring, hanya bisa diakses jika langganan aktif
    path('course/', views.course_mentoring_page, name="course_mentoring_page"),
    #path('game/', views.game, name='game'),
    path('dashboard/', views.dashboard, name='dashboard'), 
    path('langganan/', views.langganan, name='langganan'), 
    path('game/<int:pk>/', GameView.as_view(), name='game'),
    path('mengarang/', views.mengarang_view, name='mengarang'),
    path('mengarang/result/<int:pk>/', views.mengarang_result_view, name='mengarang_result'),
    path('accounts/', include('allauth.urls')),
    path('spok_game/', spok_game, name='spok_game'),
    path('spok_result/<int:session_id>/', spok_result, name='spok_result'),
    path('tentang-kami/', views.tentang_kami, name="tentang-kami"),
    path('kursus/', views.kursus, name="kursus"),
    path('video_detail/', views.video_detail, name="video_detail"),
    path('mentoring/', views.mentoring, name="mentoring"),
    path('check-subscription/', check_subscription_status, name='check_subscription_status'),
] 

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)