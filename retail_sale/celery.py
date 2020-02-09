from __future__ import absolute_import, unicode_literals
import os
from celery import Celery
from celery.schedules import crontab


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'retail_sale.settings')

app = Celery('retail_sale')

app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()

app.conf.beat_schedule = {
    'daily-db-update': {
        'task': 'web_scraper.tasks.daily_hm_db_update',
        'schedule': crontab(),
    },
}
