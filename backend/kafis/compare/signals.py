from compare.tasks import cache_table
from kafis.settings import CACHE_UPDATE_FREQ


def update_table_cache(sender, instance, created, **kwargs):
    if instance.id % CACHE_UPDATE_FREQ == 0:
        cache_table.delay(instance.not_selected.gender)