from django.test import TestCase
from rest_framework.test import APITestCase, APIClient
from django.urls import reverse
from users.models import User, Feedback
from rest_framework import status
from users.serializers import FeedbackSerializer
from rest_framework_simplejwt.tokens import RefreshToken


def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)

    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }


class Feedback_APITestCase(APITestCase):
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

        self.feedback_instance_1 = Feedback.objects.create(id=2, user_id=1, contact_back='test1',
                                                           feedback_massage='test1', status='New')
        self.feedback_instance_2 = Feedback.objects.create(id=3, user_id=2, contact_back='test2',
                                                           feedback_massage='test2', status='Current')
        self.feedback_instance_3 = Feedback.objects.create(id=4, user_id=3, contact_back='test3',
                                                           feedback_massage='test3', status='Completed')
        self.feedback_instance_4 = Feedback.objects.create(id=5, user_id=3, contact_back='test4',
                                                           feedback_massage='test4', status='Completed')

        tokens = get_tokens_for_user(self.user_instance_1)
        self.access_token = tokens['access']

    def test_get_feedback_list(self):
        # тест получение всех записей || api/v1/users/feedbacklist/
        url_list = reverse('feedback-list')
        headers = {'Authorization': f'Bearer {self.access_token}'}
        response = self.client.get(url_list, headers=headers)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        count_of_records = Feedback.objects.count()
        self.assertEqual(len(response.data), count_of_records)

        obj_from_DB = Feedback.objects.all()
        serializer_data = FeedbackSerializer(obj_from_DB, many=True).data
        self.assertEqual(serializer_data, response.data)

    def test_get_feedback_by_own_id(self):
        # получение записи по id || api/v1/contactlist/<int: pk>/
        url_by_own_id = reverse('feedback-detail', kwargs={'pk': self.feedback_instance_1.id})
        headers = {'Authorization': f'Bearer {self.access_token}'}
        response = self.client.get(url_by_own_id, headers=headers)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        serializer_data = FeedbackSerializer(self.feedback_instance_1).data
        self.assertEqual(serializer_data, response.data)

        # api/v1/users/feedbacklist/<int:pk>/ - для несуществуюшей записи. 404 должен возвращать???
        url_by_own_id = reverse('feedback-detail', kwargs={'pk': 123})
        headers = {'Authorization': f'Bearer {self.access_token}'}
        response = self.client.get(url_by_own_id, headers=headers)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual({"detail": "Not found."}, response.data)

    def test_get_feedback_by_user_id(self):
        # тест для получения записи или записей по user_id  || api/v1/users/feedbacklist/byuserid/<int: user_id>/
        url_by_user_id = r'/api/v1/users/feedbacklist/byuserid/3/'  # несколько записей
        headers = {'Authorization': f'Bearer {self.access_token}'}
        response = self.client.get(url_by_user_id, headers=headers)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        count_of_records = Feedback.objects.filter(user_id=3).count()
        self.assertEqual(len(response.data), count_of_records)

        record = Feedback.objects.filter(user_id=3)
        serializer_data = FeedbackSerializer(record, many=True).data
        self.assertEqual(serializer_data, response.data)

        url_by_user_id = r'/api/v1/users/feedbacklist/byuserid/2/'  # одна запись
        headers = {'Authorization': f'Bearer {self.access_token}'}
        response = self.client.get(url_by_user_id, headers=headers)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        count_of_records = Feedback.objects.filter(user_id=2).count()
        self.assertEqual(len(response.data), count_of_records)

        record = Feedback.objects.filter(user_id=2)
        serializer_data = FeedbackSerializer(record, many=True).data
        self.assertEqual(serializer_data, response.data)

        # тест для  получения несуществующей записи по user_id || api/v1/users/feedbacklist/byuserid/<int: user_id>/
        url_by_user_id = r'/api/v1/users/feedbacklist/byuserid/123/'  # не существующий
        headers = {'Authorization': f'Bearer {self.access_token}'}
        response = self.client.get(url_by_user_id, headers=headers)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual({"error": "записи с таким user_id не существует"}, response.data)

        url_by_user_id = r'/api/v1/users/feedbacklist/byuserid/'  # не указан user id
        headers = {'Authorization': f'Bearer {self.access_token}'}
        response = self.client.get(url_by_user_id, headers=headers)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual({"error": "введите user_id."}, response.data)

    def test_create_feedback_instance(self):
        data = {
            'user': self.user_instance_1.id,
            'feedback_massage': 'test5',
            'contact_back': 'test5',
            'status': 'New'
        }

        url = reverse('feedback-list')
        headers = {'Authorization': f'Bearer {self.access_token}'}
        response = self.client.post(url, data, format='json', headers=headers)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Feedback.objects.count(), 5)

    def test_delete_feedback_by_own(self):
        # удаление записи по id ||api/v1/users/feedbacklist/<int: pk>/
        url_by_own_id = reverse("feedback-detail", kwargs={'pk': 2})
        headers = {'Authorization': f'Bearer {self.access_token}'}
        response = self.client.delete(url_by_own_id, headers=headers)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        count_of_records = Feedback.objects.filter(pk=2).count()
        self.assertEqual(count_of_records, 0)

    def test_delete_feedback_instance_by_user_id(self):
        # удаление всех записей из таблицы Feedback,
        # привязанных к определенному user ||api/v1/users/feedbacklist/delete_by_userid/<int:user_id>/
        url_by_user_id = r'/api/v1/users/feedbacklist/delete_by_userid/3/'
        headers = {'Authorization': f'Bearer {self.access_token}'}
        response = self.client.delete(url_by_user_id, headers=headers)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        count_of_records = Feedback.objects.filter(user=3).count()
        self.assertEqual(count_of_records, 0)
        self.assertIn("Записи для пользователя с user_id 3 удалены.", response.data['success'])

    def test_delete_feedback_by_unexistence_userid(self):
        # удаление записи с несущществующим user_id
        url_by_user_id = r'/api/v1/users/feedbacklist/delete_by_userid/3231/'
        headers = {'Authorization': f'Bearer {self.access_token}'}
        response = self.client.delete(url_by_user_id, headers=headers)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertIn('Записи с таким user_id не существуют', response.data['error'])

    def test_update_feedback_instance_by_own_id(self):
        # обновление записи по id ||api/v1/users/feedbacklist/<int: pk>/
        url_by_own_id = reverse("feedback-detail", kwargs={'pk': 3})
        updated_data = {'user': 3,
                        'feedback_massage': 'Обновленное feedback_massage',
                        'status': 'Completed'}
        headers = {'Authorization': f'Bearer {self.access_token}'}

        # PUT запрос на указанный URL с обновленными данными
        response = self.client.put(url_by_own_id, updated_data, format='json', headers=headers)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Перезагружаем запись

        self.feedback_instance_2.refresh_from_db()
        self.assertEqual(self.feedback_instance_2.status, updated_data['status'])
