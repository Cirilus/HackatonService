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
    
    def test_create_team(self):
        response = self.client.post(reverse('hackaton_user_registration'), 
                               data={'id_hackaton':Hackaton.objects.all().first().pk, 'place':'1'}, format='json')

        response = self.client.post(reverse('get_my_team'), 
                               data={'id_hackaton':Hackaton.objects.all().first().pk, 'title':'test', 'description':'test'},
                               format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class GetTeamTest(APITestCase):
    def setUp(self):
        self.user_instance_1 = User.objects.create(first_name='test6', last_name='test6', 
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
        
        self.hack_user_instance = Hackaton_User.objects.create(user=self.user_instance_1,
                                                                hackaton=self.hackaton_instance, 
                                                                place=1)
        
        self.team_instance = Team.objects.create(hackaton=self.hackaton_instance, 
                                                 title='test', description='test', 
                                                 owner=self.hack_user_instance)
        self.user_team_instance = User_Team.objects.create(team=self.team_instance, 
                                                           user_id=1, is_invited=False)

        refresh = RefreshToken.for_user(self.user_instance_1)
        self.client = APIClient()
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {refresh.access_token}')
    
    def test_get_team(self):
        response = self.client.get(reverse('get_my_team'), 
                               data={'id_hackaton':'1'},
                               format='json')
        print(response.content)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class InviteTest(APITestCase):
    def setUp(self):
        self.user_instance_1 = User.objects.create(id=1, first_name='test6', last_name='test6', 
                                   middle_name='test6', email='v@mail.ru', 
                                   phone='test', password='123456789TEst', is_active = True)
        self.user_instance_2 = User.objects.create(id=2, first_name='test6', last_name='test6', 
                                   middle_name='test6', email='vb@mail.ru', 
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
        self.team_instance = Team.objects.create(id=1, hackaton_id=1, 
                                                 title='test', description='test', 
                                                 owner=self.hack_user_instance)
        self.user_team_instance = User_Team.objects.create(id=1, team_id=1, user_id=1, is_invited=False)

        refresh = RefreshToken.for_user(self.user_instance_1)
        self.client = APIClient()
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {refresh.access_token}')
    
    def test_invite_team(self):
        response = self.client.post(reverse('invite'), 
                               data={'id_hackaton':'1', 'user':'2'},
                               format='json')
        print(response.content)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
