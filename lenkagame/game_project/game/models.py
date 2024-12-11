from django.db import models


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
        return self.answer.split(',')

    def get_tags(self):
        """Mengubah kolom `tags` menjadi list."""
        return self.tags.split(',')

    def __str__(self):
        return self.title