import os
from celery import Celery
from celery.schedules import crontab


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'NewsPaper.settings',)

app = Celery('NewsPaper')
app.config_from_object('django.conf:settings', namespace='CELERY')

app.conf.beat_schedule = {
    'periodic_mailing': {
        'task': 'news.tasks.periodic_mailing',
        'schedule': crontab(hour=8, minute=0, day_of_week='monday'),
    },
}
app.autodiscover_tasks()