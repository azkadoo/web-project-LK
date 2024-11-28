from django.db import models
from django.contrib.auth.models import User

class Langganan(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    nama_lengkap = models.CharField(max_length=200)
    paket_langganan = models.CharField(max_length=200)
    start_month = models.DateField()
    end_month = models.DateField()
    is_active = models.BooleanField(default=True)
    is_premium = models.BooleanField(default=False)
