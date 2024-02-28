import os
import subprocess

from django.core.management.base import BaseCommand

from Hackaton.models import Parser_Test
import json
from app.settings import BASE_DIR


class Command(BaseCommand):
    help = 'Load hackathon data from a JSON file to the Django database'

    def run_scrapy_spider_and_copy_path(self):
        #  директория, в которой находится этот скрипт Djang
        manage_file_directory = BASE_DIR

        #  абсолютный путь к директории scrapy проекта относительно директории скрипта Django
        scrapy_project_directory = os.path.join(manage_file_directory, 'Hackaton_parser')
        path_to_save_json = os.path.join(manage_file_directory, r'Hackaton_parser/parser_result/result_parse.json')
        # переключаемся в директорию с файлом scrapy.cfg
        os.chdir(scrapy_project_directory)

        # Запускаем парсер
        scrapy_command = f'scrapy crawl hackathon_parser -O {path_to_save_json}'
        subprocess.run(scrapy_command, shell=True)

        json_file_path = os.path.join(manage_file_directory, r'Hackaton_parser/parser_result/result_parse.json')
        # Проверяем существование файла
        if os.path.exists(json_file_path):
            print(f"json-файл с хакатонами с сайта https://www.хакатоны.рф/ успешно создан. путь: {json_file_path}")
        else:
            print(f"файл не создан.")
        # Получение текущей директории

        return json_file_path

    def add_parse_data_to_db(self):
        json_file_path = self.run_scrapy_spider_and_copy_path()  # передаем путь к созданному json Файлу с хакатонами

        with open(json_file_path, encoding='utf-8') as f:
            data = json.load(f)  # открывам json файл

        num_records_added = 0  # счетчик добавленных записей

        for item_data in data:  # идем по json
            for item in item_data:

                if item_data[item] is None:
                    item_data[item] = 'empty'

                # обработка значений-списоков из json файла (призовой фонд и целевая аудитория ) нужна из-за особеннотей парсинга
                if isinstance(item_data[item], list):
                    item_data[item] = '\n'.join(item_data[item])


            is_online = 'онлайн' in item_data['location'].lower()  # True если хакатон проводится онлайн

            # создаем объект в бд если нет такого объекта
            hackathon, created = Parser_Test.objects.get_or_create(
                title=item_data['title'],
                defaults={
                    'image_url': item_data['image_url'],
                    'creator': item_data.get('creator', 'empty'),
                    'grand_prize': item_data.get('grand_prize', 'empty'),
                    'end_registration': item_data.get('end_registration', 'empty'),
                    'about': item_data.get('description', 'empty'),
                    'target_audience': item_data.get('roles', 'empty'),
                    'date_hackaton': item_data.get('start-end', 'empty'),
                    'location': item_data.get('location', 'empty'),
                    'is_online': is_online,
                    'hackaton_link': item_data.get('url', 'empty'),
                }
            )

            if created:
                num_records_added += 1

        self.stdout.write(
            self.style.SUCCESS(f'Данные успешно загружены в базу данных. Внесено записей: {num_records_added}'))

    # запускаем
    def handle(self, *args, **options):
        self.add_parse_data_to_db()
