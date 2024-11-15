from django.urls import path
from lensakata_app import views

urlpatterns = [
    path('',views.index, name='index')
]