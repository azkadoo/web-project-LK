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
