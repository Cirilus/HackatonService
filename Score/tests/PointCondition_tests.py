from django.test import TestCase
from rest_framework.test import APITestCase, APIClient
from django.urls import reverse
from Score.models import HistoryPoint, PointCondition
from django.contrib.auth.models import User # пока со стандартным пользователем связываемся
from rest_framework import status
from Score.serializers import PointConditionSerializer, HistoryPointSerializer
import json

class PointCondition_APITestCase(APITestCase):
    def setUp(self):
        #тестовые данные
        self.client = APIClient()

        self.user_instance = User.objects.create_user(id=1, username='test', password='test', email='test@test.com')
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
        url_by_own_id = reverse('pointcondition-detail' , kwargs={'pk': self.point_condition_instance_1.id})
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
        #тест для получения записи или записей по user_id || api/v1/pointconditionlist/byuserid/<int:user_id> //
        url_by_user_id = '/api/v1/pointconditionlist/byuserid/1/'
        response = self.client.get(url_by_user_id)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        count_of_records = PointCondition.objects.filter(user_id__isnull=False).count()
        self.assertEqual(count_of_records, len(response.data))

        #или вот такая проверка, как лучше?????
        records = PointCondition.objects.filter(user_id=1)
        serializer_data = PointConditionSerializer(records, many=True).data
        self.assertEqual(serializer_data, response.data)

        # тест для  получения несуществующей записи по user_id || api/v1/pointconditionlist/byuserid/<int:user_id> //
        url_by_user_id = '/api/v1/pointconditionlist/byuserid/2/' # не существующий
        response = self.client.get(url_by_user_id)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual([], response.data)

class PointCondition_SerializersTestCase(TestCase):
    def setUp(self):
        self.user_instance = User.objects.create_user(id=1, username='test', password='test', email='test@test.com')
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