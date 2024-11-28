from django.urls import path
from . import views

# import class View

urlpatterns = [
    path('loginn/', views.login_view, name='loginn'),
    path('home/', views.home, name='home'),
    path('login/', views.login, name='login'),
]