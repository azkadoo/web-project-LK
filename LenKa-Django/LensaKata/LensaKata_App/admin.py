from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(ReviewCard)
admin.site.register(Story)
admin.site.register(GameSession)
admin.site.register(UserProgress)
admin.site.register(Subscription)


class VideoDetailInline(admin.TabularInline):
    model = VideoDetail
    extra = 1  # Menampilkan form kosong untuk input video baru

@admin.register(Kursus)
class KursusAdmin(admin.ModelAdmin):
    list_display = ['judul', 'created_at']
    inlines = [VideoDetailInline]

@admin.register(VideoDetail)
class VideoDetailAdmin(admin.ModelAdmin):
    list_display = ['judul_video', 'kursus', 'created_at']
