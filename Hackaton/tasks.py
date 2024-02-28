from apscheduler.schedulers.background import BackgroundScheduler

import os
from app import settings


# @shared_task
# def run_parser_task():
#     os.chdir(BASE_DIR)
#     call_command('python manage.py load_hackathon_data')


# функция - задание
def run_scrapy_and_db_update():
    os.chdir(settings.BASE_DIR)
    os.system('python manage.py load_hackathon_data')
    print('TASK EXECUTED')

#тестовая таска
# def prompt():
#     print("Executing Task...")
from apscheduler.triggers.cron import CronTrigger
#планировкщик
def setup_parser_scheduler():
    # Создает ФОНОВЫЙ планировщик
    scheduler = BackgroundScheduler()
    # планирование задания
    # scheduler.add_job(run_scrapy_and_db_update, 'interval', seconds=30) #интервальный запуск

    scheduler.add_job(
        run_scrapy_and_db_update,
        trigger=CronTrigger(hour=9, minute=50, second=0, timezone='Europe/Moscow')
    ) #запуск в определенное время

    # Запуск запланированных заданий
    scheduler.start()

