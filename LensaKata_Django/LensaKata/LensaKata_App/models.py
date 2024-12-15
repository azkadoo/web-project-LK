from django.db import models
from django import forms
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import timedelta, datetime
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
        return [tag.strip() for tag in self.tags.split(',')]

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

class SPOKChallenge(models.Model):
    sentence = models.CharField(max_length=255, help_text="Masukkan kalimat lengkap untuk tantangan")
    subject = models.CharField(max_length=100, help_text="Jawaban untuk Subjek")
    predicate = models.CharField(max_length=100, help_text="Jawaban untuk Predikat")
    object = models.CharField(max_length=100, help_text="Jawaban untuk Objek")
    description = models.CharField(max_length=100, help_text="Jawaban untuk Keterangan")

    def __str__(self):
        return f"Tantangan: {self.sentence}"

class SPOKSession(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    challenge = models.ForeignKey(SPOKChallenge, on_delete=models.CASCADE)
    score = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Sesi {self.user.username} - Tantangan: {self.challenge.sentence}"

class Subscription(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    is_active = models.BooleanField(default=False)
    start_date = models.DateTimeField(null=True, blank=True)
    end_date = models.DateTimeField(null=True, blank=True)

    def activate_subscription(self, months):
        """Aktifkan langganan untuk durasi tertentu."""
        now = timezone.now()
        self.is_active = True
        self.start_date = now
        self.end_date = now + timedelta(days=30 * months)  # Durasi 30 hari per bulan
        self.save()

    def is_subscription_valid(self):
        """Cek apakah langganan masih aktif dan belum kedaluwarsa."""
        if self.is_active and self.end_date:
            return self.end_date > timezone.now()
        return False

    def __str__(self):
        return f"{self.user.username} - Aktif: {self.is_active}"

# Model untuk Kursus
class Kursus(models.Model):
    judul = models.CharField(max_length=255)
    deskripsi = models.TextField()
    gambar = models.ImageField(upload_to='kursus_images/',blank=True, null=True)  # Gambar disimpan di media/kursus_images/
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.judul

# Model untuk Video Detail
class VideoDetail(models.Model):
    kursus = models.ForeignKey(Kursus, on_delete=models.CASCADE, related_name='video_details')
    judul_video = models.CharField(max_length=255)
    deskripsi_video = models.TextField()
    video_url = models.URLField()  # URL Video YouTube atau lainnya
    durasi = models.CharField(max_length=50, null=True, blank=True)  # Contoh: "10 Menit"
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.judul_video