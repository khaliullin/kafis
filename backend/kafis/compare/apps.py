from django.apps import AppConfig
from django.db.models.signals import post_save


class CompareConfig(AppConfig):
    name = 'compare'

    def ready(self):
        from .models import Compare
        from .signals import update_table_cache
        post_save.connect(update_table_cache, sender=Compare)
