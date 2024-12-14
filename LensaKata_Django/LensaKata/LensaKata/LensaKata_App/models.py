from django.db import models
from django import forms
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import *

# Create your models here.
class ReviewCard(models.Model):
    name = models.CharField(max_length=100)
    image = models.ImageField(upload_to='review_images/')
    text = models.TextField()
    
    def __str__(self):
        return self.name

class Paketlangganan(models.Model):
    id_paket = models.BigAutoField(auto_created=True, primary_key=True),
    paket = models.CharField(max_length=50)
    harga = models.IntegerField()
    deskripsi = models.CharField(max_length=200, default='')
    status = models.CharField(max_length=20, default='Aktif')

class Story(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    question = models.CharField(max_length=300)
    answer = models.TextField(
        help_text="Pisahkan jawaban dengan koma, contoh: bidadari,telaga,Jaka Tarub")
    tags = models.TextField(
        help_text="Pisahkan tag dengan koma, contoh: langit,menangis,telaga")

    def get_answers(self):
        """Mengubah kolom `answer` menjadi list."""
        return [ans.strip() for ans in self.answer.split(',')]  # Do not apply .lower()

    def get_keywords(self):
        """Mengubah kolom `tags` menjadi list kata kunci."""
        return [tag.strip().lower() for tag in self.tags.split(',')]

    def __str__(self):
        return self.title

class GameSession(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    score = models.IntegerField()
    matched_keywords = models.TextField()  # Store as a comma-separated string or JSON
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Session for {self.user.username} - Score: {self.score}"

class UserProgress(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    challenges_completed = models.IntegerField(default=0)
    daily_score = models.IntegerField(default=0)  # Tambahkan ini
    daily_words_learned = models.IntegerField(default=0)  # Tambahkan ini
    daily_challenges_completed = models.IntegerField(default=0)  # Tambahkan ini
    
    def __str__(self):
        return f"{self.user.username} - Challenges Completed: {self.challenges_completed}"
    
class GameChallenge(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)  # Allow null values
    content = models.TextField()  # Konten cerita yang ditulis oleh pengguna
    score = models.IntegerField(null=True, blank=True)  # Skor yang dihitung berdasarkan cerita
    created_at = models.DateTimeField(auto_now_add=True)  # Waktu pembuatan cerita

    def __str__(self):
        return f"GameChallenge at {self.created_at}"

    def save(self, *args, **kwargs):
        # Skor dihitung sebelum menyimpan objek
        self.score = calculate_score(self.content)  # Menyimpan skor berdasarkan isi cerita
        super().save(*args, **kwargs)

def calculate_score(content):
    """
    Fungsi sederhana untuk menghitung skor berdasarkan panjang cerita.
    Skor akan lebih tinggi untuk cerita yang lebih panjang.
    """
    word_count = len(content.split())  # Menghitung jumlah kata dalam cerita
    if word_count < 50:
        return 10  # Skor rendah untuk cerita pendek
    elif word_count < 100:
        return 20  # Skor menengah untuk cerita sedang
    else:
        return 30  # Skor tinggi untuk cerita panjang

class StoryRating(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    game_challenge = models.ForeignKey(GameChallenge, on_delete=models.CASCADE)
    rating = models.IntegerField(choices=[(1, '1 Star'), (2, '2 Stars'), (3, '3 Stars'), (4, '4 Stars'), (5, '5 Stars')])

    class Meta:
        unique_together = ('user', 'game_challenge')  # Pastikan satu user hanya bisa memberi satu rating per cerita

    def __str__(self):
        return f"{self.user.username} rated {self.game_challenge.content} - {self.rating} Stars"