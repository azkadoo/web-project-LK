from django.db import models
from django.contrib.auth.models import User


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


# class GameSPOKSession(models.Model):
#     user = models.ForeignKey(User, on_delete=models.CASCADE)
#     example_sentence = models.CharField(max_length=300)  # Contoh kalimat
#     subject = models.CharField(max_length=100, blank=True)
#     predicate = models.CharField(max_length=100, blank=True)
#     object = models.CharField(max_length=100, blank=True)
#     complement = models.CharField(max_length=100, blank=True)
#     score = models.IntegerField(default=0)  # Skor permainan
#     created_at = models.DateTimeField(auto_now_add=True)

#     def calculate_score(self, correct_answers):
#         score = 0
#         if self.subject.lower() in correct_answers.get('subject', []):
#             score += 5
#         if self.predicate.lower() in correct_answers.get('predicate', []):
#             score += 5
#         if self.object.lower() in correct_answers.get('object', []):
#             score += 5
#         if self.complement.lower() in correct_answers.get('complement', []):
#             score += 5
#         return score

#     def __str__(self):
#         return f"SPOK Game Session - {self.user.username} - Score: {self.score}"
