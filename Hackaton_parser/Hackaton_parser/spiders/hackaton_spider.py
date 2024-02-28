import scrapy


# парсер для создания json дока
class HackathonSpider(scrapy.Spider):
    name = 'hackathon_parser'
    start_urls = ['https://www.хакатоны.рф/']

    custom_settings = {
        'FEED_FORMAT': 'json',  # Формат файла
        'FEED_EXPORT_ENCODING': 'utf-8',

    }

    def parse(self, response):
        # Проходим по каждой ссылке с классом 'js-product-link'
        for product_link in response.css('a.js-product-link'):
            # Извлекаем текстовые элементы из описания хакатона
            text_elements = product_link.css('.t776__descr.t-descr.t-descr_xxs *::text').extract()

            hack_dating = text_elements[2]  # даты проведения хакатона
            if any(year in hack_dating for year in ['2022', '2021',
                                                    '2020']):  # оптимизация - не проводим все операции ниже для хакатонов которые были давно
                continue  # на 10 миллисекунд быстрее:)

            data = {}  # пустой словарь чтобы складывать данные
            current_key = None



            #если элемент начинается с интересующей нас строки то обновляем ключ для словаря и потом именно в этот ключ все записываем
            # как только другой ключ появится он обнулится
            # Итерируем по текстовым элементам
            for element in text_elements:
                if element.strip():
                    if element.startswith('Хакатон'):
                        current_key = 'start-end'
                    elif element.startswith('Регистрация'):
                        current_key = 'end_registration'
                    elif element.startswith('Организатор'):
                        current_key = 'creator'
                    elif element.startswith('Технологический фокус'):
                        current_key = 'description'
                    elif element.startswith('Призовой фонд'):
                        current_key = 'grand_prize'
                        # Используем список для хранения значений призового фонда так как их может быть много разделенных тегами br
                        data[current_key] = []
                    elif element.startswith('Целевая аудитория'):
                        current_key = 'roles'
                        # Используем список для хранения значений целевой аудитории так как их может быть много разделенных тегами br
                        data[current_key] = []
                    elif current_key:
                        # Заменяем символы, которые могут повлиять на json
                        element = element.replace('"', "'")
                        # Если это призовой фонд, добавляем элемент в список
                        #может для всех такое сделать
                        if current_key == 'grand_prize':
                            data[current_key].append(element)
                        elif current_key == 'roles':
                            data[current_key].append(element)
                        else:
                            # Записываем значение в структуру данных
                            data[current_key] = element
                            current_key = None

            hack_title = product_link.css(
                '.t776__title.js-product-name div::text').get()  # получаем название хакатона текстом

            if hack_title == None:  # костыль, разобраться и поправить потом
                continue

            # Если ключ 'Хакатон' есть и содержит '2024', то возвращаем данные
            # проверка годов на вхождение в даты проведения хакатона
            if 'start-end' in data and '2024' in data['start-end'] or \
                    any(year in hack_title for year in ['2024', '24']):  # проверка годов на вхождение в title

                # ДОБАВИТЬ ДРУГИЕ ПРОВЕРКИ ПО НЕОБХОДИМОСТИ

                yield {
                    'url': product_link.css('::attr(href)').extract_first(),
                    'image_url': product_link.css('.t776__imgwrapper div.t776__bgimg::attr(data-original)').get(),
                    'title': product_link.css('.t776__title.js-product-name div::text').get(),
                    'location': product_link.css('.t776__descr::text').extract_first(),
                    **data,  # Добавляем все ключи из data в основной словарь

                }

# cd Hackaton_parser
# scrapy crawl hackathon -o output.json
# команды для запуска кроулера

# scrapy runspider Hackaton_parser/Hackaton_parser/spiders/hackaton_spider.py
