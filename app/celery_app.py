import os
import time

from celery import Celery
from django.conf import settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'app.settings')

app = Celery('app')
app.config_from_object('django.conf:settings')
app.conf.broker_url = settings.CELERY_BROKER_URL



app.autodiscover_tasks() #ищем все файлы tasks.py во всех django приложениях

@app.task()
def debug_task():
    time.sleep(20)
    print('hello from debug_task')
