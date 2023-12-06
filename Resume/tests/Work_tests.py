from django.test import TestCase
from rest_framework.test import APITestCase, APIClient
from django.urls import reverse
from Resume.models import Work, Resume
from users.models import User
from rest_framework import status
from Resume.serializers import WorkSerializer
import json


class WorkByResume_APITestCase(APITestCase):
    # тесты для апишки в целом (для списка записей операции удаления добавлеия редактирования создания)
    def setUp(self):
        # тестовые данные
        # разобраться с полем created Выкидывает ворнинги касательно часового пояса
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

        self.work_instance_1 = Work.objects.create(id=2, resume_id=1, title='test1', description='test1')
        self.work_instance_2 = Work.objects.create(id=3, resume_id=2, title='test2', description='test2')
        self.work_instance_3 = Work.objects.create(id=4, resume_id=1, title='test3', description='test3')

    def test_get_work_list(self):
        # тест получение всех записей || api/v1/worklist/
        url_list = reverse('work-list')
        response = self.client.get(url_list)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        count_of_records = Work.objects.count()
        self.assertEqual(len(response.data), count_of_records)

        obj_from_DB = Work.objects.all()
        serializer_data = WorkSerializer(obj_from_DB, many=True).data
        self.assertEqual(serializer_data, response.data)

    def test_get_work_by_own_id(self):
        # получение записи по id || api/v1/worklist/<int: pk>/
        url_by_own_id = reverse('work-detail', kwargs={'pk': self.work_instance_1.id})
        response = self.client.get(url_by_own_id)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        serializer_data = WorkSerializer(self.work_instance_1).data
        self.assertEqual(serializer_data, response.data)

        # api/v1/worklist/<int:pk>/ - для несуществуюшей записи. 404 должен возвращать???
        url_by_own_id = reverse('work-detail', kwargs={'pk': 7})
        response = self.client.get(url_by_own_id)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual({"detail": "Not found."}, response.data)

    def test_get_work_by_resume_id(self):
        # тест для получения записи или записей по resume_id  || api/v1/worklist/byresumeid/<int: resume_id>/
        url_by_resume_id = '/api/v1/worklist/byresumeid/1/'
        response = self.client.get(url_by_resume_id)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        record = Work.objects.filter(resume_id=1)
        serializer_data = WorkSerializer(record, many=True).data
        self.assertEqual(serializer_data, response.data)

        # тест для  получения несуществующей записи по resume_id || api/v1/contactlist/byuserid/<int: user_id>/
        url_by_resume_id = '/api/v1/worklist/byresumeid/11/'  # не существующий
        response = self.client.get(url_by_resume_id)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual({"error": "записи с таким resume_id не существует"}, response.data)

    def test_create_work(self):
        # тест добавление записи в модель work|| api/v1/worklist/
        data = {
            "resume": 3,
            "title": "test4",
            'description': 'test4',
        }
        #
        url = reverse("work-list")
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Work.objects.count(), 4)

    #
    def test_delete_work_by_own(self):
        # удаление записи по id ||api/v1/worklist/<int: pk>/
        url_by_resume_id = url = reverse("work-detail", kwargs={'pk': 3})
        response = self.client.delete(url_by_resume_id)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        count_of_records = Work.objects.filter(resume_id=2).count()
        self.assertEqual(count_of_records, 0)

    #
    def test_update_work_by_own_id(self):
        # обновление записи по id ||api/v1/worklist/<int: pk>/
        url_by_resume_id = reverse("work-detail", kwargs={'pk': 3})
        updated_data = {'resume': 2, ''
                        'title': 'Обновленное work',
                        'description': 'Обновленное work'}
        # PUT запрос на указанный URL с обновленными данными
        response = self.client.put(url_by_resume_id, updated_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Перезагружаем запись
        self.work_instance_2.refresh_from_db()
        self.assertEqual(self.work_instance_2.title, updated_data['title'])


#
class Work_SerializersTestCase(TestCase):
    def setUp(self):
        # тестовые данные
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

        self.work_instance_1 = Work.objects.create(id=1, resume_id=1, title='test1', description='test1')
        self.work_instance_2 = Work.objects.create(id=2, resume_id=2, title='test2', description='test2')
        # fields = ['resume', 'id', 'title', 'description', 'begin', 'end']

    def test_serializer_for_work(self):
        data_for_test = Work.objects.all()
        serialized_data = WorkSerializer(data_for_test, many=True).data
        serialized_data = json.loads(json.dumps(serialized_data))

        expected_data = [
            {
                'resume': self.work_instance_1.resume_id,
                'title': self.work_instance_1.title,
                'id': self.work_instance_1.id,
                'description': self.work_instance_1.description,
                'begin': self.work_instance_1.begin,
                'end': self.work_instance_1.end,

            },
            {
                'resume': self.work_instance_2.resume_id,
                'title': self.work_instance_2.title,
                'id': self.work_instance_2.id,
                'description': self.work_instance_2.description,
                'begin': self.work_instance_2.begin,
                'end': self.work_instance_2.end,

            },

        ]

        self.assertEqual(expected_data, serialized_data)
