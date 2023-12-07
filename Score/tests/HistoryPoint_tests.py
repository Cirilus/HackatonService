from django.test import TestCase
from rest_framework.test import APITestCase, APIClient
from django.urls import reverse
from Score.models import HistoryPoint, PointCondition
from users.models import User
from rest_framework import status
from Score.serializers import HistoryPointSerializer
import json


# Create your tests here.
# тесты для api приложения Score. Таблица HistoryPoint


class HistoryPoint_APITestCase(APITestCase):
    def setUp(self):
        # тестовые данные
        # разобраться с полем created Выкидывает ворнинги касательно часового пояса
        self.client = APIClient()

        self.user_instance_1 = User.objects.create(id=1,first_name='test1', last_name='test1',
                                   middle_name='test1', email='test1@test.ru',
                                   phone='test1', password='test1', is_active = True)
        self.user_instance_2 = User.objects.create(id=2,first_name='test2', last_name='test2',
                                   middle_name='test2', email='test2@test.ru',
                                   phone='test2', password='test2', is_active = True)
        self.user_instance_3 = User.objects.create(id=3,first_name='test3', last_name='test3',
                                   middle_name='test3', email='test3@test.ru',
                                   phone='test3', password='test3', is_active = True)

        self.point_condition_instance_1 = PointCondition.objects.create(id=1, title='test1')
        self.point_condition_instance_2 = PointCondition.objects.create(id=2, user_id=1, title='test2')
        self.point_condition_instance_3 = PointCondition.objects.create(id=3, user_id=2, title='test3')
        self.point_condition_instance_4 = PointCondition.objects.create(id=4, user_id=2, title='test4')

        self.history_point_instance_1 = HistoryPoint.objects.create(id=2, user_id=1, condition_id=1, count=1, )
        self.history_point_instance_2 = HistoryPoint.objects.create(id=3, user_id=2, condition_id=2, count=2, )
        self.history_point_instance_3 = HistoryPoint.objects.create(id=4, user_id=2, condition_id=3, count=3, )

    def test_API_for_historypoint_list(self):
        # тест получение всех записей || api/v1/historypointlist/
        url_list = reverse('historypoint-list')
        response = self.client.get(url_list)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        count_of_records = HistoryPoint.objects.count()
        self.assertEqual(response.data['count'], count_of_records)

        obj_from_DB = HistoryPoint.objects.all()
        serializer_data = HistoryPointSerializer(obj_from_DB, many=True).data
        self.assertEqual(len(serializer_data), response.data['count'])

    def test_API_for_historypoint_detail(self):
        # тест получения записи по собственному id || api/v1/historypointlist/<int:pk>
        url_by_own_id = reverse('historypoint-detail', kwargs={'pk': self.history_point_instance_1.id})
        response = self.client.get(url_by_own_id)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        serializer_data = HistoryPointSerializer(self.history_point_instance_1).data
        self.assertEqual(serializer_data, response.data)

        # api/v1/historypointlist/<int:pk>/ - для несуществуюшей записи. 404 должен возвращать???
        url_by_own_id = reverse('pointcondition-detail', kwargs={'pk': 123})
        response = self.client.get(url_by_own_id)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual({"detail": "Not found."}, response.data)

    def test_API_for_historypoint_byuserid(self):
        # тест для получения записи или записей по user_id  || api/v1/historypointlist/byuserid/<int:user_id> //
        url_by_user_id = '/api/v1/historypointlist/byuserid/1/'
        response = self.client.get(url_by_user_id)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        count_of_records = HistoryPoint.objects.filter(user_id=1).count()
        self.assertEqual(count_of_records, len(response.data))

        # или вот такая проверка, как лучше?????
        records = HistoryPoint.objects.filter(user_id=1)
        serializer_data = HistoryPointSerializer(records, many=True).data
        self.assertEqual(serializer_data, response.data)

        url_by_user_id = '/api/v1/historypointlist/byuserid/2/'
        response = self.client.get(url_by_user_id)
        records = HistoryPoint.objects.filter(user_id=2)
        serializer_data = HistoryPointSerializer(records, many=True).data
        self.assertEqual(serializer_data, response.data)

        # тест для  получения несуществующей записи по user_id || api/v1/pointconditionlist/byuserid/<int:user_id> //
        url_by_user_id = '/api/v1/historypointlist/byuserid/3/'  # не существующий
        response = self.client.get(url_by_user_id)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual([], response.data)

    def test_API_for_historypoint_bycondition(self):
        # тест для получения записи по condition_id || api/v1/historypointlist/bycondition/<int:condition_id> //
        url_by_user_id = '/api/v1/historypointlist/bycondition/1/'
        response = self.client.get(url_by_user_id)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        count_of_records = HistoryPoint.objects.filter(condition_id=1).count()
        self.assertEqual(count_of_records, len(response.data))

        # или вот такая проверка, как лучше?????
        records = HistoryPoint.objects.filter(condition_id=1)
        serializer_data = HistoryPointSerializer(records, many=True).data
        self.assertEqual(serializer_data, response.data)

        url_by_user_id = '/api/v1/historypointlist/bycondition/2/'
        response = self.client.get(url_by_user_id)
        records = HistoryPoint.objects.filter(condition_id=2)
        serializer_data = HistoryPointSerializer(records, many=True).data
        self.assertEqual(serializer_data, response.data)

        # тест для  получения несуществующей записи по user_id api/v1/historypointlist/byuserid/<int:user_id> //
        url_by_user_id = '/api/v1/historypointlist/bycondition/4/'  # не существующий
        response = self.client.get(url_by_user_id)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual([], response.data)

    def test_create_historypoint_by_own_id(self):
        # тест добавление записи в модель historypoint|| api/v1/historypointlist/
        data = {
            'id': 5,
            "user": 2,
            "condition": 4,
            'count': 43,
        }

        url = reverse("historypoint-list")
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(HistoryPoint.objects.count(), 4)

    def test_delete_historypoint_by_own_id(self):
        # Получаем URL для удаления historypoint по его ID || api/v1/historypointlist/
        url_to_delete = reverse('historypoint-detail', kwargs={'pk': self.history_point_instance_2.id})

        # отправляем DELETE-запрос на указанный URL
        response = self.client.delete(url_to_delete)

        # проверяем, что удаление прошло успешно (HTTP статус 204 No Content)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        # Убеждаемся, что запись больше не существует в базе данных
        self.assertFalse(HistoryPoint.objects.filter(id=self.history_point_instance_2.id).exists())
        self.assertEqual(HistoryPoint.objects.count(), 2)

    def test_update_historypoint_by_own_id(self):
        # Получаем URL для обновления резюме по его ID || api/v1/historypointlist/
        url_to_update = reverse('historypoint-detail', kwargs={'pk': self.history_point_instance_2.id})

        updated_data = {'count': 60}

        # patch запрос на указанный URL с обновленными данными
        response = self.client.patch(url_to_update, updated_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Перезагружаем запись
        self.history_point_instance_2.refresh_from_db()
        self.assertEqual(self.history_point_instance_2.count, updated_data['count'])


class HistoryPoint_SerializersTestCase(TestCase):
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
        self.point_condition_instance_2 = PointCondition.objects.create(id=3, user_id=2, title='test3')

        self.history_point_instance_1 = HistoryPoint.objects.create(id=1, user_id=1, condition_id=1, count=1,
                                                                    created=None)
        self.history_point_instance_2 = HistoryPoint.objects.create(id=2, user_id=2, condition_id=2, count=2,
                                                                    created=None)
        self.history_point_instance_3 = HistoryPoint.objects.create(id=3, user_id=2, condition_id=3, count=3,
                                                                    created=None)

    def test_serializer_for_historypoint(self):
        data_for_test = HistoryPoint.objects.all()
        serialized_data = HistoryPointSerializer(data_for_test, many=True).data
        serialized_data = json.loads(json.dumps(serialized_data))
        expected_data = [
            {
                'user': self.history_point_instance_1.user_id,
                'count': self.history_point_instance_1.count,
                'id': self.history_point_instance_1.id,
                'condition': self.history_point_instance_1.condition_id,
                'created': self.history_point_instance_1.created,
            },
            {
                'user': self.history_point_instance_2.user_id,
                'count': self.history_point_instance_2.count,
                'id': self.history_point_instance_2.id,
                'condition': self.history_point_instance_2.condition_id,
                'created': self.history_point_instance_2.created,
            },
            {
                'user': self.history_point_instance_3.user_id,
                'count': self.history_point_instance_3.count,
                'id': self.history_point_instance_3.id,
                'condition': self.history_point_instance_3.condition_id,
                'created': self.history_point_instance_3.created,
            }
        ]

        self.assertEqual(expected_data, serialized_data)
