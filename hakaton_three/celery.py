import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'hakaton_three.settings')

app = Celery('hakaton_three')
app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()
