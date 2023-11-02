from django.test import TestCase
from rest_framework.test import APITestCase, APIClient
from django.urls import reverse
from Score.models import HistoryPoint, PointCondition
from django.contrib.auth.models import User # пока со стандартным пользователем связываемся
from rest_framework import status
from Score.serializers import PointConditionSerializer, HistoryPointSerializer
import json

# Create your tests here.
#тесты для api приложения Score. Таблица HistoryPoint


class HistoryPoint_APITestCase(APITestCase):
    def setUp(self):
        # тестовые данные
        #разобраться с полем created Выкидывает ворнинги касательно часового пояса
        self.client = APIClient()

        self.user_instance = User.objects.create_user(id=1, username='test', password='test', email='test@test.com')
        self.user_instance = User.objects.create_user(id=2, username='test2', password='test2', email='test2@test.com')

        self.point_condition_instance_1 = PointCondition.objects.create(id=1, title='test1')
        self.point_condition_instance_2 = PointCondition.objects.create(id=2, user_id=1, title='test2')
        self.point_condition_instance_2 = PointCondition.objects.create(id=3, user_id=2, title='test3')


        self.history_point_instance_1 = HistoryPoint.objects.create(id=1, user_id=1, condition_id=1, count=1, )
        self.history_point_instance_2 = HistoryPoint.objects.create(id=2, user_id=2, condition_id=2, count=2, )
        self.history_point_instance_3 = HistoryPoint.objects.create(id=3, user_id=2, condition_id=3, count=3, )
    def test_API_for_historypoint_list(self):
        # тест получение всех записей || api/v1/historypointlist/
        url_list = reverse('historypoint-list')
        response = self.client.get(url_list)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        count_of_records = HistoryPoint.objects.count()
        self.assertEqual(len(response.data), count_of_records)

        obj_from_DB = HistoryPoint.objects.all()
        serializer_data = HistoryPointSerializer(obj_from_DB, many=True).data
        self.assertEqual(serializer_data, response.data)


    def test_API_for_historypoint_detail(self):

        #тест получения записи по собственному id || api/v1/historypointlist/<int:pk>
        url_by_own_id = reverse('historypoint-detail' , kwargs={'pk': self.history_point_instance_1.id})
        response = self.client.get(url_by_own_id)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        serializer_data = HistoryPointSerializer(self.history_point_instance_1).data
        self.assertEqual(serializer_data, response.data)


        # api/v1/historypointlist/<int:pk>/ - для несуществуюшей записи. 404 должен возвращать???
        url_by_own_id = reverse('pointcondition-detail', kwargs={'pk': 4})
        response = self.client.get(url_by_own_id)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual({"detail": "Not found."}, response.data)

    def test_API_for_historypoint_byuserid(self):

        #тест для получения записи или записей по user_id  || api/v1/historypointlist/byuserid/<int:user_id> //
        url_by_user_id = '/api/v1/historypointlist/byuserid/1/'
        response = self.client.get(url_by_user_id)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        count_of_records = HistoryPoint.objects.filter(user_id=1).count()
        self.assertEqual(count_of_records, len(response.data))

        #или вот такая проверка, как лучше?????
        records = HistoryPoint.objects.filter(user_id=1)
        serializer_data = HistoryPointSerializer(records, many=True).data
        self.assertEqual(serializer_data, response.data)

        url_by_user_id = '/api/v1/historypointlist/byuserid/2/'
        response = self.client.get(url_by_user_id)
        records = HistoryPoint.objects.filter(user_id=2)
        serializer_data = HistoryPointSerializer(records, many=True).data
        self.assertEqual(serializer_data, response.data)


        # тест для  получения несуществующей записи по user_id || api/v1/pointconditionlist/byuserid/<int:user_id> //
        url_by_user_id = '/api/v1/historypointlist/byuserid/3/' # не существующий
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

class HistoryPoint_SerializersTestCase(TestCase):
    def setUp(self):


        self.user_instance = User.objects.create_user(id=1, username='test', password='test', email='test@test.com')
        self.user_instance = User.objects.create_user(id=2, username='test2', password='test2', email='test2@test.com')

        self.point_condition_instance_1 = PointCondition.objects.create(id=1, title='test1')
        self.point_condition_instance_2 = PointCondition.objects.create(id=2, user_id=1, title='test2')
        self.point_condition_instance_2 = PointCondition.objects.create(id=3, user_id=2, title='test3')

        self.history_point_instance_1 = HistoryPoint.objects.create(id=1, user_id=1, condition_id=1, count=1, created=None)
        self.history_point_instance_2 = HistoryPoint.objects.create(id=2, user_id=2, condition_id=2, count=2, created=None)
        self.history_point_instance_3 = HistoryPoint.objects.create(id=3, user_id=2, condition_id=3, count=3, created=None )
    def test_serializer_for_historypoint(self):
        data_for_test = HistoryPoint.objects.all()
        serialized_data = HistoryPointSerializer(data_for_test, many=True).data
        serialized_data = json.loads(json.dumps(serialized_data))
        expected_data = [
            {
                'user_id': self.history_point_instance_1.user_id,
                'count': self.history_point_instance_1.count,
                'id': self.history_point_instance_1.id,
                'condition_id': self.history_point_instance_1.condition_id,
                'created' : self.history_point_instance_1.created,
            },
            {
                'user_id': self.history_point_instance_2.user_id,
                'count': self.history_point_instance_2.count,
                'id': self.history_point_instance_2.id,
                'condition_id': self.history_point_instance_2.condition_id,
                'created': self.history_point_instance_2.created,
            },
            {
                'user_id': self.history_point_instance_3.user_id,
                'count': self.history_point_instance_3.count,
                'id': self.history_point_instance_3.id,
                'condition_id': self.history_point_instance_3.condition_id,
                'created': self.history_point_instance_3.created,
            }
        ]

        self.assertEqual(expected_data, serialized_data)