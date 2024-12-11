# mengarang/models.py

from django.db import models


class GameChallenge(models.Model):
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
