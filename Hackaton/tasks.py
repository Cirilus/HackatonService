import multiprocessing

from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
import os

from app import settings


# функция - задание
def run_scrapy_and_db_update():
    os.chdir(settings.BASE_DIR)
    os.system('python manage.py load_hackathon_data')
    print('TASK EXECUTED')

#создание нового процесса для выполнения асинхронно от основного процесса
def run_scrapy_and_db_update_async():
    process = multiprocessing.Process(target=run_scrapy_and_db_update)
    process.start()
    process.join()

#планировкщик
def setup_parser_scheduler():
    # Создает ФОНОВЫЙ планировщик
    scheduler = BackgroundScheduler()
    # планирование задания
    # scheduler.add_job(run_scrapy_and_db_update_async, 'interval', seconds=30) #интервальный запуск

    scheduler.add_job(
        run_scrapy_and_db_update_async,
        trigger=CronTrigger(hour=8, minute=0, second=0, timezone='Europe/Moscow')
    ) #запуск в определенное время

    # Запуск запланированных заданий
    scheduler.start()

