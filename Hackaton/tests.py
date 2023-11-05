from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIRequestFactory, force_authenticate, APIClient
from rest_framework.authtoken.models import Token
from rest_framework_simplejwt.tokens import RefreshToken
from .models import Hackaton, Hackaton_User, Team, User_Team
from .serializers import HackatonSerializer
from rest_framework.authtoken.models import Token
from users.models import User


class GetHackatonsTest(APITestCase):
    def setUp(self):
        self.user_instance = User.objects.create(first_name='test6', last_name='test6', 
                                   middle_name='test6', email='v@mail.ru', 
                                   phone='test', password='123456789TEst', is_active = True)

        self.hackaton_instance = Hackaton.objects.create(title='test1', imageUrl='', 
                                description='test',
                                descriptionShort='test',
                                creator='test',
                                start_registration='2023-10-23T21:48:27Z',
                                end_registration='2023-10-23T21:48:27Z',
                                start='2023-10-23T21:48:27Z',
                                end='2023-10-23T21:48:27Z')

        refresh = RefreshToken.for_user(self.user_instance)
        self.client = APIClient()
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {refresh.access_token}')

    def test_get_hackaton(self):
        response = self.client.get(reverse('get_hackatons'), data={'id':'1'}, format='json')
        serializer = HackatonSerializer(Hackaton.objects.all(), many=True)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_create_hackaton_user(self):
        response = self.client.post(reverse('hackaton_user_registration'), 
                               data={'id_hackaton':Hackaton.objects.all().first().pk, 'place':'1'}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class TeamTest(APITestCase):
    def setUp(self):
        self.user_instance = User.objects.create(id=1, first_name='test6', last_name='test6', 
                                   middle_name='test6', email='v@mail.ru', 
                                   phone='test', password='123456789TEst', is_active = True)

        self.hackaton_instance = Hackaton.objects.create(id=1, title='test1', imageUrl='', 
                                description='test',
                                descriptionShort='test',
                                creator='test',
                                start_registration='2023-10-23T21:48:27Z',
                                end_registration='2023-10-23T21:48:27Z',
                                start='2023-10-23T21:48:27Z',
                                end='2023-10-23T21:48:27Z')

        self.hack_user_instance = Hackaton_User.objects.create(id=1, user_id=1, hackaton_id=1, place=1)
        self.team_instance = Team.objects.create(id=1, hackaton_id=1, title='test', description='test', owner=self.hack_user_instance)
        refresh = RefreshToken.for_user(self.user_instance)
        self.client = APIClient()
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {refresh.access_token}')

    def test_create_team(self):
        response = self.client.post(reverse('get_team'), 
                            data={'id_hackaton':"1", 'title':'test', 'description':'test'},
                            format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        

# class KickLeaveTest(APITestCase):
#     def setUp(self):
#         self.user_instance_1 = User.objects.create(id=1, first_name='test6', last_name='test6', middle_name='test6', email='v@mail.ru', phone='test', password='123456789TEst', is_active = True)
#         self.user_instance_2 = User.objects.create(id=2, first_name='test6', last_name='test6', middle_name='test6', email='vb@mail.ru', phone='test', password='123456789TEst', is_active = True)
        
#         self.hackaton_instance = Hackaton.objects.create(id=1, title='test1', imageUrl='', description='test', descriptionShort='test', creator='test', start_registration='2023-10-23T21:48:27Z', end_registration='2023-10-23T21:48:27Z', start='2023-10-23T21:48:27Z', end='2023-10-23T21:48:27Z')
#         self.hackaton_instance = Hackaton.objects.create(id=2, title='test1', imageUrl='', description='test', descriptionShort='test', creator='test', start_registration='2023-10-23T21:48:27Z', end_registration='2023-10-23T21:48:27Z', start='2023-10-23T21:48:27Z', end='2023-10-23T21:48:27Z')

#         #юзеры первого хакатона
#         self.hack_user_instance = Hackaton_User.objects.create(id=1, user_id=1, hackaton_id=1, place=1)
#         self.hack_user_instance_2 = Hackaton_User.objects.create(id=2, user_id=2, hackaton_id=1, place=1)

#         #юзеры второго хакатона
#         self.hack_user_instance_3 = Hackaton_User.objects.create(id=3, user_id=1, hackaton_id=2, place=1)
#         self.hack_user_instance_4 = Hackaton_User.objects.create(id=4, user_id=2, hackaton_id=2, place=1)


#         self.team_instance = Team.objects.create(id=1, hackaton_id=1, title='test', description='test', owner=self.hack_user_instance)
#         self.team_instance = Team.objects.create(id=2, hackaton_id=2, title='test', description='test', owner=self.hack_user_instance_4)

#         #участники команды на первом хакатоне
#         self.user_team_instance = User_Team.objects.create(id=1, team_id=1, user_id=1, is_invited=False)
#         self.user_team_instance = User_Team.objects.create(id=2, team_id=1, user_id=2, is_invited=False)

#         #участники команды на первом хакатоне
#         self.user_team_instance = User_Team.objects.create(id=3, team_id=2, user_id=3, is_invited=False)
#         self.user_team_instance = User_Team.objects.create(id=4, team_id=2, user_id=4, is_invited=False)

#         refresh = RefreshToken.for_user(self.user_instance_1)
#         self.client = APIClient()
#         self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {refresh.access_token}')

#     def test_kick_from_team(self):
#         response = self.client.delete(reverse('kick_user'), 
#                                data={'id_hackaton':'1', 'user':'2'},
#                                format='json')
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
    
#     def test_kick_from_team(self):
#         response = self.client.delete(reverse('kick_user'), 
#                                data={'id_hackaton':'2', 'user':'2'},
#                                format='json')
#         self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

# class InviteTest(APITestCase):
#     def setUp(self):
#         self.user_instance_1 = User.objects.create(id=1, first_name='test6', last_name='test6', 
#                                    middle_name='test6', email='v@mail.ru', 
#                                    phone='test', password='123456789TEst', is_active = True)
#         self.user_instance_2 = User.objects.create(id=2, first_name='test6', last_name='test6', 
#                                    middle_name='test6', email='vb@mail.ru', 
#                                    phone='test', password='123456789TEst', is_active = True)
        
#         self.hackaton_instance = Hackaton.objects.create(id=1, title='test1', imageUrl='', 
#                                 description='test',
#                                 descriptionShort='test',
#                                 creator='test',
#                                 start_registration='2023-10-23T21:48:27Z',
#                                 end_registration='2023-10-23T21:48:27Z',
#                                 start='2023-10-23T21:48:27Z',
#                                 end='2023-10-23T21:48:27Z')
        
#         self.hack_user_instance = Hackaton_User.objects.create(id=1, user_id=1, hackaton_id=1, place=1)
#         self.hack_user_instance_2 = Hackaton_User.objects.create(id=2, user_id=2, hackaton_id=1, place=1)


#         self.team_instance = Team.objects.create(id=1, hackaton_id=1, 
#                                                  title='test', description='test', 
#                                                  owner=self.hack_user_instance)
        
#         self.user_team_instance = User_Team.objects.create(id=1, team_id=1, user_id=1, is_invited=False)

#         refresh = RefreshToken.for_user(self.user_instance_1)
#         self.client = APIClient()
#         self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {refresh.access_token}')
    
#     def test_invite_team(self):
#         response = self.client.post(reverse('invite'), 
#                                data={'id_hackaton':'1', 'user':'2'},
#                                format='json')
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
    
#     def test_url_invite_team(self):
#         response = self.client.post(reverse('invite_url'), 
#                                data={'id_hackaton':'1'},
#                                format='json')
        
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
    

    

