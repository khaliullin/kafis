from django.db.models.signals import post_save
from django.dispatch import receiver

from compare.models import Compare


@receiver(post_save, sender=Compare)
def update_table_cache(sender, instance, created, **kwargs):
    pass