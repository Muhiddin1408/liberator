from django.core.cache import cache
from django.db.models.signals import post_delete, post_save
from django.dispatch import receiver

from app.context_processors import MENU_CACHE_KEY
from app.models import ServiceCategory


@receiver([post_save, post_delete], sender=ServiceCategory)
def clear_menu_cache(**kwargs):
    cache.delete(MENU_CACHE_KEY)
