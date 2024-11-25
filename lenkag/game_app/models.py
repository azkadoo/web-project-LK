from django.db import models


class Story(models.Model):
    title = models.CharField(max_length=100)
    paragraph = models.TextField()

    def __str__(self):
        return self.title


class GameSession(models.Model):
    story = models.ForeignKey(Story, on_delete=models.CASCADE)
    user_input = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Session for Story: {self.story.title}"
