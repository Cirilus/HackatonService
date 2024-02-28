import os
import time

from celery import Celery
from django.conf import settings
from celery.schedules import crontab
from datetime import timedelta


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'app.settings')

app = Celery('app')
app.config_from_object('django.conf:settings')
app.conf.broker_url = settings.CELERY_BROKER_URL




app.autodiscover_tasks() #ищем все файлы tasks.py во всех django приложениях

@app.task()
def debug_task():
    time.sleep(20)
    print('hello from debug_task')


@app.task()
def run_scrapy_and_db_update_celery():
    os.chdir(settings.BASE_DIR)
    os.system('python manage.py load_hackathon_data')
    print('TASK EXECUTED')


app.conf.beat_schedule = {
    'run-every-morning': {
        'task': 'app.celery_app.run_scrapy_and_db_update_celery',
        'schedule': timedelta(minutes=1),
    },

} #запуск в интервал


# app.conf.beat_schedule = {
#     'run-every-morning': {
#         'task': '.Hackaton.tasks.run_scrapy_and_db_update_celery',
#         'schedule': crontab(hour=19, minute=50, second=0, timezone='Europe/Moscow'),
#     },
#
# } запуск в определенное время





