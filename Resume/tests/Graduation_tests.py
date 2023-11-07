from django.test import TestCase
from rest_framework.test import APITestCase, APIClient
from django.urls import reverse
from Resume.models import Graduation
from rest_framework import status
from Resume.serializers import GraduationSerializer
import json


#
class Graduation_APITestCase(APITestCase):
    # тесты для апишки в целом (для списка записей операции удаления добавлеия редактирования создания)
    def setUp(self):
        # тестовые данные
        self.client = APIClient()

        self.graduation_instance_1 = Graduation.objects.create(id=1, title='Бакалавриат')
        self.graduation_instance_2 = Graduation.objects.create(id=2, title='Магистратура')
        self.graduation_instance_3 = Graduation.objects.create(id=3, title='Аспирантура')

    def test_get_graduation_list(self):
        # тест получение всех записей || api/v1/graduationlist/
        url_list = reverse('graduation-list')
        response = self.client.get(url_list)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        count_of_records = Graduation.objects.count()
        self.assertEqual(len(response.data), count_of_records)

        obj_from_DB = Graduation.objects.all()
        serializer_data = GraduationSerializer(obj_from_DB, many=True).data
        self.assertEqual(serializer_data, response.data)

    def test_get_graduation_by_own_id(self):
        # получение записи по id || api/v1/graduationlist/<int: pk>/
        url_by_own_id = reverse('graduation-detail', kwargs={'pk': self.graduation_instance_1.id})
        response = self.client.get(url_by_own_id)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        serializer_data = GraduationSerializer(self.graduation_instance_1).data
        self.assertEqual(serializer_data, response.data)

        # api/v1/graduationlist/<int:pk>/ - для несуществуюшей записи. 404 должен возвращать???
        url_by_own_id = reverse('graduation-detail', kwargs={'pk': 4})
        response = self.client.get(url_by_own_id)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual({"detail": "Not found."}, response.data)

    def test_create_graduation(self):
        # тест добавление записи в модель graduation|| api/v1/graduationlist/

        data = {
            'id': 4,
            'title': 'Школа'
        }

        url = reverse("graduation-list")
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Graduation.objects.count(), 4)

    def test_delete_graduation_by_own(self):
        # удаление записи по id ||api/v1/graduationlist/<int: pk>/
        url_by_resume_id = url = reverse("graduation-detail", kwargs={'pk': 3})
        response = self.client.delete(url_by_resume_id)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        count_of_records = Graduation.objects.filter(title='Аспирантура').count()
        self.assertEqual(count_of_records, 0)

    def test_update_graduation_by_own_id(self):
        # обновление записи по id ||api/v1/graduationlist/<int: pk>/
        url_by_resume_id = reverse("graduation-detail", kwargs={'pk': 3})
        updated_data = {
            'title': 'Обновленное graduation',
        }

        # PUT запрос на указанный URL с обновленными данными
        response = self.client.put(url_by_resume_id, updated_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Перезагружаем запись
        self.graduation_instance_3.refresh_from_db()
        self.assertEqual(self.graduation_instance_3.title, updated_data['title'])


#
class Graduation_SerializersTestCase(TestCase):
    def setUp(self):
        self.graduation_instance_1 = Graduation.objects.create(id=1, title='Бакалавриат')
        self.graduation_instance_2 = Graduation.objects.create(id=2, title='Магистратура')
        self.graduation_instance_3 = Graduation.objects.create(id=3, title='Аспирантура')

    def test_serializer_for_education(self):
        data_for_test = Graduation.objects.all()
        serialized_data = GraduationSerializer(data_for_test, many=True).data
        serialized_data = json.loads(json.dumps(serialized_data))

        # мб захардкодить данные ?
        expected_data = [
            {
                'title': self.graduation_instance_1.title,
                'id': self.graduation_instance_1.id,
            },
            {
                'title': self.graduation_instance_2.title,
                'id': self.graduation_instance_2.id,
            },
            {
                'title': self.graduation_instance_3.title,
                'id': self.graduation_instance_3.id,
            }

        ]

        self.assertEqual(expected_data, serialized_data)
