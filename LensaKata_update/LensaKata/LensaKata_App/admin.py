from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(ReviewCard)
admin.site.register(Story)
admin.site.register(GameSession)
admin.site.register(UserProgress)