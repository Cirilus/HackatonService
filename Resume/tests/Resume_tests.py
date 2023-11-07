from django.test import TestCase
from rest_framework.test import APITestCase, APIClient
from django.urls import reverse
from Resume.models import Resume
from django.contrib.auth.models import User  # пока со стандартным пользователем связываемся
from rest_framework import status
from Resume.serializers import ResumeSerializer
import json
# Create your tests here.
class Resume_APITestCase(APITestCase):
    # тесты для апишки в целом (для списка записей операции удаления добавлеия редактирования создания)
    def setUp(self):
        # тестовые данные
        # разобраться с полем created Выкидывает ворнинги касательно часового пояса
        self.client = APIClient()

        self.user_instance_1 = User.objects.create_user(id=1, username='test', password='test', email='test@test.com')
        self.user_instance_2 = User.objects.create_user(id=2, username='test2', password='test2',
                                                        email='test2@test.com')
        self.user_instance_3 = User.objects.create_user(id=3, username='test3', password='test3',
                                                        email='test3@test.com')

        self.resume_instance_1 = Resume.objects.create(id=1, user_id=1, title='test1', description='test1')
        self.resume_instance_2 = Resume.objects.create(id=2, user_id=2, title='test2', description='test2')

    def test_get_resume_list(self):
        # тест получение всех записей || api/v1/resumelist/
        url_list = reverse('resume-list')
        response = self.client.get(url_list)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        count_of_records = Resume.objects.count()
        self.assertEqual(len(response.data), count_of_records)

        obj_from_DB = Resume.objects.all()
        serializer_data = ResumeSerializer(obj_from_DB, many=True).data
        self.assertEqual(serializer_data, response.data)

    def test_get_resume_by_id(self):
        # получение записи по id || api/v1/resumelist/<int: pk>/
        url_by_own_id = reverse('resume-detail', kwargs={'pk': self.resume_instance_1.id})
        response = self.client.get(url_by_own_id)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        serializer_data = ResumeSerializer(self.resume_instance_1).data
        self.assertEqual(serializer_data, response.data)

        # api/v1/resumelist/<int:pk>/ - для несуществуюшей записи. 404 должен возвращать???
        url_by_own_id = reverse('resume-detail', kwargs={'pk': 4})
        response = self.client.get(url_by_own_id)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual({"detail": "Not found."}, response.data)

    def test_create_resume(self):
        # тест добавление записи в модель resume|| api/v1/resumelist/
        data = {
            'id': 3,
            "user": 3,
            "title": "test3",
            'description': 'test3',
        }

        url = reverse("resume-list")
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Resume.objects.count(), 3)

    def test_delete_resume(self):
        # Получаем URL для удаления резюме по его ID
        url_to_delete = reverse('resume-detail', kwargs={'pk': self.resume_instance_2.id})

        # отправляем DELETE-запрос на указанный URL
        response = self.client.delete(url_to_delete)

        # проверяем, что удаление прошло успешно (HTTP статус 204 No Content)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        # Убеждаемся, что запись больше не существует в базе данных
        self.assertFalse(Resume.objects.filter(id=self.resume_instance_2.id).exists())
        self.assertEqual(Resume.objects.count(), 1)

    def test_update_resume(self):
        # Получаем URL для обновления резюме по его ID
        url_to_update = reverse('resume-detail', kwargs={'pk': self.resume_instance_2.id})

        updated_data = {'title': 'Обновленное резюме'}

        # patch запрос на указанный URL с обновленными данными
        response = self.client.patch(url_to_update, updated_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Перезагружаем запись
        self.resume_instance_2.refresh_from_db()
        self.assertEqual(self.resume_instance_2.title, updated_data['title'])


class Resumebyuserid_APITestCase(APITestCase):
    # тесты для REsume получение удаление редактирование записей по user_id || api/v1/resumelist/byuserid/<int: user_id>/
    def setUp(self):
        # тестовые данные
        # разобраться с полем created Выкидывает ворнинги касательно часового пояса
        self.client = APIClient()

        self.user_instance_1 = User.objects.create_user(id=1, username='test', password='test', email='test@test.com')
        self.user_instance_2 = User.objects.create_user(id=2, username='test2', password='test2',
                                                        email='test2@test.com')
        self.user_instance_3 = User.objects.create_user(id=3, username='test3', password='test3',
                                                        email='test3@test.com')

        self.resume_instance_1 = Resume.objects.create(id=1, user_id=1, title='test1', description='test1')
        self.resume_instance_2 = Resume.objects.create(id=2, user_id=2, title='test2', description='test2')

    def test_get_resume_by_userid(self):
        # тест для получения записи или записей по user_id  || api/v1/resumelist/byuserid/<int: user_id>/
        url_by_user_id = '/api/v1/resumelist/byuserid/1/'
        response = self.client.get(url_by_user_id)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        count_of_records = Resume.objects.filter(user_id=1).count()
        self.assertEqual(count_of_records, len(response.data))

        # или вот такая проверка, как лучше?????
        records = Resume.objects.filter(user_id=1)
        serializer_data = ResumeSerializer(records, many=True).data
        self.assertEqual(serializer_data, response.data)

        url_by_user_id = '/api/v1/resumelist/byuserid/2/'
        response = self.client.get(url_by_user_id)
        records = Resume.objects.filter(user_id=2)
        serializer_data = ResumeSerializer(records, many=True).data
        self.assertEqual(serializer_data, response.data)

        # тест для  получения несуществующей записи по user_id || api/v1/resumelist/byuserid/<int: user_id>/
        url_by_user_id = '/api/v1/resumelist/byuserid/10/'  # не существующий
        response = self.client.get(url_by_user_id)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual({"error": "Резюме с таким user_id не существует."}, response.data)

    def test_delete_resume_by_userid(self):
        # получение записи по id ||api/v1/resumelist/byuserid/<int: user_id>/
        url_by_user_id = '/api/v1/resumelist/byuserid/1/'
        response = self.client.delete(url_by_user_id)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        count_of_records = Resume.objects.filter(user_id=1).count()
        self.assertEqual(count_of_records, 0)

    def test_update_resume_by_userid(self):
        url_by_user_id = '/api/v1/resumelist/byuserid/1/'
        updated_data = {'user': 1, ''
                                   'title': 'Обновленное резюме',
                        'description': 'Обновленное резюме'}
        # PUT запрос на указанный URL с обновленными данными
        response = self.client.put(url_by_user_id, updated_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Перезагружаем запись
        self.resume_instance_1.refresh_from_db()
        self.assertEqual(self.resume_instance_1.title, updated_data['title'])


class Resume_SerializersTestCase(TestCase):
    # сериалайзер тест
    def setUp(self):
        self.user_instance_1 = User.objects.create_user(id=1, username='test', password='test', email='test@test.com')
        self.user_instance_2 = User.objects.create_user(id=2, username='test2', password='test2',
                                                        email='test2@test.com')
        self.user_instance_3 = User.objects.create_user(id=3, username='test3', password='test3',
                                                        email='test3@test.com')

        self.resume_instance_1 = Resume.objects.create(id=1, user_id=1, title='test1', description='test1')
        self.resume_instance_2 = Resume.objects.create(id=2, user_id=2, title='test2', description='test2')

    # fields = ['user', 'title', 'description', 'visible', 'id']
    def test_serializer_for_resume(self):
        data_for_test = Resume.objects.all()
        serialized_data = ResumeSerializer(data_for_test, many=True).data
        serialized_data = json.loads(json.dumps(serialized_data))
        expected_data = [
            {
                'user': self.resume_instance_1.user_id,
                'title': self.resume_instance_1.title,
                'id': self.resume_instance_1.id,
                'description': self.resume_instance_1.description,
                'visible': self.resume_instance_1.visible,
            },
            {
                'user': self.resume_instance_2.user_id,
                'title': self.resume_instance_2.title,
                'id': self.resume_instance_2.id,
                'description': self.resume_instance_2.description,
                'visible': self.resume_instance_2.visible,
            },

        ]

        self.assertEqual(expected_data, serialized_data)
