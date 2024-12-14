# utils.py

from django.conf import settings

def get_user_level(score):
    # Iterasi melalui setiap threshold level yang ada di konfigurasi settings.LEVEL_THRESHOLDS
    for index, threshold in enumerate(settings.LEVEL_THRESHOLDS):
        # Jika score lebih kecil dari threshold saat ini, maka return level saat ini
        if score < threshold:
            return index + 1 
        
    # Jika skor pengguna lebih besar dari semua threshold,
    # maka pengguna berada di level terakhir + 1 (level tambahan setelah semua thresholds).
    return len(settings.LEVEL_THRESHOLDS) + 1