from django.test import TestCase
from rest_framework.test import APITestCase, APIClient
from django.urls import reverse
from Resume.models import Hackatons, Resume
from users.models import User
from rest_framework import status
from Resume.serializers import HackatonsSerializer
import json


class HackatonsByResume_APITestCase(APITestCase):
    # тесты для апишки в целом (для списка записей операции удаления добавлеия редактирования создания)
    def setUp(self):
        # тестовые данные
        # разобраться с полями-датами Выкидывает ворнинги касательно часового пояса + коммент в модели оставил
        self.client = APIClient()

        self.user_instance_1 = User.objects.create(id=1, first_name='test1', last_name='test1',
                                                   middle_name='test1', email='test1@test.ru',
                                                   phone='test1', password='test1', is_active=True)
        self.user_instance_2 = User.objects.create(id=2, first_name='test2', last_name='test2',
                                                   middle_name='test2', email='test2@test.ru',
                                                   phone='test2', password='test2', is_active=True)
        self.user_instance_3 = User.objects.create(id=3, first_name='test3', last_name='test3',
                                                   middle_name='test3', email='test3@test.ru',
                                                   phone='test3', password='test3', is_active=True)

        self.resume_instance_1 = Resume.objects.create(id=1, user_id=1, title='test1', description='test1')
        self.resume_instance_2 = Resume.objects.create(id=2, user_id=2, title='test2', description='test2')
        self.resume_instance_3 = Resume.objects.create(id=3, user_id=3, title='test3', description='test3')

        self.hackatons_instance_1 = Hackatons.objects.create(id=2, resume_id=1, title='test1', description='test3',
                                                             place=1)
        self.hackatons_instance_2 = Hackatons.objects.create(id=3, resume_id=2, title='test2', description='test2',
                                                             place=2)
        self.hackatons_instance_3 = Hackatons.objects.create(id=4, resume_id=2, title='test3', description='test3',
                                                             place=3)

    def test_get_hackatons_list(self):
        # тест получение всех записей || api/v1/hackatonslist/
        url_list = reverse('hackatons-list')
        response = self.client.get(url_list)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        count_of_records = Hackatons.objects.count()
        self.assertEqual(response.data['count'], count_of_records)

        obj_from_DB = Hackatons.objects.all()
        serializer_data = HackatonsSerializer(obj_from_DB, many=True).data
        self.assertEqual(len(serializer_data), response.data['count'])

    #
    def test_get_hackatons_by_own_id(self):
        # получение записи по id || api/v1/hackatonslist/<int: pk>/
        url_by_own_id = reverse('hackatons-detail', kwargs={'pk': self.hackatons_instance_1.id})
        response = self.client.get(url_by_own_id)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        serializer_data = HackatonsSerializer(self.hackatons_instance_1).data
        self.assertEqual(serializer_data, response.data)

        # api/v1/hackatonslist/<int:pk>/ - для несуществуюшей записи. 404 должен возвращать???
        url_by_own_id = reverse('hackatons-detail', kwargs={'pk': 52})
        response = self.client.get(url_by_own_id)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual({"detail": "Not found."}, response.data)

    def test_get_hackatons_by_resume_id(self):
        # тест для получения записи или записей по resume_id  || api/v1/hackatonslist/byresumeid/<int: resume_id>/
        url_by_resume_id = '/api/v1/hackatonslist/byresumeid/2/'
        response = self.client.get(url_by_resume_id)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        record = Hackatons.objects.filter(resume_id=2)
        serializer_data = HackatonsSerializer(record, many=True).data
        self.assertEqual(serializer_data, response.data)

        # тест для  получения несуществующей записи по resume_id || api/v1/hackatonslist/byuserid/<int: user_id>/
        url_by_resume_id = '/api/v1/hackatonslist/byresumeid/11/'  # не существующий
        response = self.client.get(url_by_resume_id)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual({"error": "записи с таким resume_id не существует."}, response.data)

    def test_create_hackatons(self):
        # тест добавление записи в модель hackatons|| api/v1/hackatonslist/
        data = {
            'id': 4,
            "resume": 2,
            "title": "test4",
            'description': 'test4',
            'place': 4
        }

        url = reverse("hackatons-list")
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Hackatons.objects.count(), 4)

    #
    def test_delete_hackatons_by_own(self):
        # удаление записи по id ||api/v1/hackatonslist/<int: pk>/
        url_by_resume_id = reverse("hackatons-detail", kwargs={'pk': 2})
        response = self.client.delete(url_by_resume_id)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        count_of_records = Hackatons.objects.filter(resume_id=1).count()
        self.assertEqual(count_of_records, 0)

    def test_update_hackatons_by_own_id(self):
        # обновление записи по id ||api/v1/hackatonslist/<int: pk>/
        url_by_resume_id = reverse("hackatons-detail", kwargs={'pk': 3})
        updated_data = {'resume': 3,
                        'title': 'Обновленное hackatons',
                        'description': 'Обновленное hackatons',
                        'place': 10}

        # PUT запрос на указанный URL с обновленными данными
        response = self.client.put(url_by_resume_id, updated_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Перезагружаем запись
        self.hackatons_instance_2.refresh_from_db()
        self.assertEqual(self.hackatons_instance_2.title, updated_data['title'])


#
class Hackatons_SerializersTestCase(TestCase):
    def setUp(self):
        # тестовые данные
        self.client = APIClient()

        self.user_instance_1 = User.objects.create(id=1, first_name='test1', last_name='test1',
                                                   middle_name='test1', email='test1@test.ru',
                                                   phone='test1', password='test1', is_active=True)
        self.user_instance_2 = User.objects.create(id=2, first_name='test2', last_name='test2',
                                                   middle_name='test2', email='test2@test.ru',
                                                   phone='test2', password='test2', is_active=True)
        self.user_instance_3 = User.objects.create(id=3, first_name='test3', last_name='test3',
                                                   middle_name='test3', email='test3@test.ru',
                                                   phone='test3', password='test3', is_active=True)

        self.resume_instance_1 = Resume.objects.create(id=1, user_id=1, title='test1', description='test1')
        self.resume_instance_2 = Resume.objects.create(id=2, user_id=2, title='test2', description='test2')
        self.resume_instance_2 = Resume.objects.create(id=3, user_id=3, title='test3', description='test3')

        self.hackatons_instance_1 = Hackatons.objects.create(id=1, resume_id=1, title='test1', description='test3',
                                                             place=1)
        self.hackatons_instance_2 = Hackatons.objects.create(id=2, resume_id=2, title='test3', description='test3',
                                                             place=2)
        self.hackatons_instance_3 = Hackatons.objects.create(id=3, resume_id=2, title='test3', description='test3',
                                                             place=3)

    def test_serializer_for_hackatons(self):
        data_for_test = Hackatons.objects.all()
        serialized_data = HackatonsSerializer(data_for_test, many=True).data
        serialized_data = json.loads(json.dumps(serialized_data))

        expected_data = [
            {
                'resume': self.hackatons_instance_1.resume_id,
                'title': self.hackatons_instance_1.title,
                'id': self.hackatons_instance_1.id,
                'description': self.hackatons_instance_1.description,
                'place': self.hackatons_instance_1.place,
                'begin': self.hackatons_instance_1.begin,
                'end': self.hackatons_instance_1.end,

            },
            {
                'resume': self.hackatons_instance_2.resume_id,
                'title': self.hackatons_instance_2.title,
                'id': self.hackatons_instance_2.id,
                'description': self.hackatons_instance_2.description,
                'place': self.hackatons_instance_2.place,
                'begin': self.hackatons_instance_2.begin,
                'end': self.hackatons_instance_2.end,

            },
            {
                'resume': self.hackatons_instance_3.resume_id,
                'title': self.hackatons_instance_3.title,
                'id': self.hackatons_instance_3.id,
                'description': self.hackatons_instance_3.description,
                'place': self.hackatons_instance_3.place,
                'begin': self.hackatons_instance_3.begin,
                'end': self.hackatons_instance_3.end,
            }

        ]

        self.assertEqual(expected_data, serialized_data)
