from django.db import models
from django import forms

# Create your models here.
class Member(models.Model):
  firstname = models.CharField(max_length=255)
  lastname = models.CharField(max_length=255)
  phone = models.IntegerField(null=True)
  joined_date = models.DateField(null=True)

class ReviewCard(models.Model):
    name = models.CharField(max_length=100)
    image = models.ImageField(upload_to='review_images/')
    text = models.TextField()
    
    def __str__(self):
        return self.name

class FormName(forms.Form):
  name = forms.CharField()
  email = forms.EmailField()
  text = forms.CharField(widget=forms.Textarea)