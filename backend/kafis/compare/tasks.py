from celery import shared_task

from compare.helpers import set_table_cache


@shared_task
def cache_table(compare):
    set_table_cache(compare)