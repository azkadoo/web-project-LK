# LensaKata_App/custom_tags.py
from django import template

register = template.Library()

@register.filter
def get(dictionary, key):
    """Mengambil item dari dictionary berdasarkan key."""
    return dictionary.get(key)