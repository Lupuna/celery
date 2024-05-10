from celery import Celery
import os


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'site_and_parser.settings')


app = Celery('site_and_parser')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()


# app.conf.beat_schedule = {
#     'get_categories_every_one_minutes': {
#         'task': 'src.main.tasks.get_api',
#         'schedule': crontab(minute='*/1')
#     },
# }