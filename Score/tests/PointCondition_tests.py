from django.test import TestCase
from rest_framework.test import APITestCase, APIClient
from django.urls import reverse
from Score.models import PointCondition
from users.models import User
from rest_framework import status
from Score.serializers import PointConditionSerializer
import json


class PointCondition_APITestCase(APITestCase):
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

        self.point_condition_instance_1 = PointCondition.objects.create(id=1, title='test1')
        self.point_condition_instance_2 = PointCondition.objects.create(id=2, user_id=1, title='test2')
        self.point_condition_instance_3 = PointCondition.objects.create(id=3, user_id=1, title='test3')

    def test_API_for_pointcondition_list(self):
        # тест получение всех записей || api/v1/pointconditionlist/
        url_list = reverse('pointcondition-list')
        response = self.client.get(url_list)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        count_of_records = PointCondition.objects.count()
        self.assertEqual(len(response.data), count_of_records)

        obj_from_DB = PointCondition.objects.all()
        serializer_data = PointConditionSerializer(obj_from_DB, many=True).data
        self.assertEqual(serializer_data, response.data)

    def test_API_for_pointcondition_detail(self):
        # тест получения записи по собственному id || api/v1/pointconditionlist/<int:pk>
        url_by_own_id = reverse('pointcondition-detail', kwargs={'pk': self.point_condition_instance_1.id})
        response = self.client.get(url_by_own_id)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        serializer_data = PointConditionSerializer(self.point_condition_instance_1).data
        self.assertEqual(serializer_data, response.data)

        # api/v1/pointconditionlist/<int:pk>/ - для несуществуюшей записи. 404 должен возвращать???
        url_by_own_id = reverse('pointcondition-detail', kwargs={'pk': 4})
        response = self.client.get(url_by_own_id)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual({"detail": "Not found."}, response.data)

    def test_API_for_pointcondition_byuserid(self):
        # тест для получения записи или записей по user_id || api/v1/pointconditionlist/byuserid/<int:user_id> //
        url_by_user_id = '/api/v1/pointconditionlist/byuserid/1/'
        response = self.client.get(url_by_user_id)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        count_of_records = PointCondition.objects.filter(user_id__isnull=False).count()
        self.assertEqual(count_of_records, len(response.data))

        # или вот такая проверка, как лучше?????
        records = PointCondition.objects.filter(user_id=1)
        serializer_data = PointConditionSerializer(records, many=True).data
        self.assertEqual(serializer_data, response.data)

        # тест для  получения несуществующей записи по user_id || api/v1/pointconditionlist/byuserid/<int:user_id> //
        url_by_user_id = '/api/v1/pointconditionlist/byuserid/2/'  # не существующий
        response = self.client.get(url_by_user_id)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual([], response.data)
        # (id=3, user_id=1, title='test3')

    def test_create_pointcondition_by_own_id(self):
        # тест добавление записи в модель pointcondtition|| api/v1/pointcondtitionlist/
        data = {
            'id': 4,
            "user": 2,
            "title": 'test4',
        }

        url = reverse("pointcondition-list")
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(PointCondition.objects.count(), 4)

    def test_delete_pointcondition_by_own_id(self):
        # Получаем URL для удаления historypoint по его ID || api/v1/pointcondtitionlist/
        url_to_delete = reverse('pointcondition-detail', kwargs={'pk': self.point_condition_instance_2.id})

        # отправляем DELETE-запрос на указанный URL
        response = self.client.delete(url_to_delete)

        # проверяем, что удаление прошло успешно (HTTP статус 204 No Content)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        # Убеждаемся, что запись больше не существует в базе данных
        self.assertFalse(PointCondition.objects.filter(id=self.point_condition_instance_2.id).exists())
        self.assertEqual(PointCondition.objects.count(), 2)

    #
    def test_update_pointcondition_by_own_id(self):
        # Получаем URL для обновления резюме по его ID || api/v1/pointcondtitionlist/
        url_to_update = reverse('pointcondition-detail', kwargs={'pk': self.point_condition_instance_2.id})

        updated_data = {'title': 'викторина'}

        # patch запрос на указанный URL с обновленными данными
        response = self.client.patch(url_to_update, updated_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Перезагружаем запись
        self.point_condition_instance_2.refresh_from_db()
        self.assertEqual(self.point_condition_instance_2.title, updated_data['title'])


class PointCondition_SerializersTestCase(TestCase):
    def setUp(self):
        self.user_instance_1 = User.objects.create(id=1, first_name='test1', last_name='test1',
                                                   middle_name='test1', email='test1@test.ru',
                                                   phone='test1', password='test1', is_active=True)
        self.user_instance_2 = User.objects.create(id=2, first_name='test2', last_name='test2',
                                                   middle_name='test2', email='test2@test.ru',
                                                   phone='test2', password='test2', is_active=True)
        self.user_instance_3 = User.objects.create(id=3, first_name='test3', last_name='test3',
                                                   middle_name='test3', email='test3@test.ru',
                                                   phone='test3', password='test3', is_active=True)
        self.point_condition_instance_1 = PointCondition.objects.create(id=1, title='test1')
        self.point_condition_instance_2 = PointCondition.objects.create(id=2, user_id=1, title='test2')
        self.point_condition_instance_3 = PointCondition.objects.create(id=3, user_id=1, title='test3')

    def test_serializer_for_pointcondition(self):
        data_for_test = PointCondition.objects.all()
        serialized_data = PointConditionSerializer(data_for_test, many=True).data
        serialized_data = json.loads(json.dumps(serialized_data))
        expected_data = [
            {
                'user': self.point_condition_instance_1.user_id,
                'title': self.point_condition_instance_1.title,
                'id': self.point_condition_instance_1.id,
            },
            {
                'user': self.point_condition_instance_2.user_id,
                'title': self.point_condition_instance_2.title,
                'id': self.point_condition_instance_2.id,
            },
            {
                'user': self.point_condition_instance_3.user_id,
                'title': self.point_condition_instance_3.title,
                'id': self.point_condition_instance_3.id,
            }
        ]

        self.assertEqual(expected_data, serialized_data)
