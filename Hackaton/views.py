
from users.models import User
from rest_framework.views import APIView
from rest_framework import generics, mixins, filters
from rest_framework.viewsets import ReadOnlyModelViewSet, ViewSet
from .serializers import HackatonUserSerializer, ListTeamSerializer, UserTeamSerializer, HackatonSerializer, TeamSerializer
from rest_framework.response import Response
from django.forms.models import model_to_dict
from .models import User_Team, Team, Hackaton_User, Hackaton
from rest_framework.permissions import AllowAny, IsAuthenticatedOrReadOnly, IsAuthenticated
from .queries import GetHackaton, GetHackatonUser, GetTeam, GetUserTeam, DeleteUserTeam
import jwt
from django.core.cache import cache
import uuid
from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiExample, OpenApiResponse, OpenApiRequest
from drf_spectacular.types import OpenApiTypes


#регистрация пользователя на хакатон по id

class HackatonUserView(APIView):
    permission_classes = [IsAuthenticated,]
    @extend_schema(
        tags=['Hackaton user'],
        description='Регистрация на хакатон',
        request=OpenApiRequest(),
        responses={200: OpenApiTypes.OBJECT, 404: OpenApiTypes.OBJECT},
        examples=[OpenApiExample(name='Example create hackaton_user', value={'result': 'заебца'}, response_only=True, status_codes=[200]),
                  OpenApiExample(name='Example create hackaton_user', value={'error': 'не заебца'}, response_only=True, status_codes=[404]),
                  OpenApiExample(name='Example create hackaton_user', value={'id_hackaton': '1',}, request_only=True),
        ],
    )
    def post(self, request):
        request.data['user'] = request.user.pk
        request.data['hackaton'] = request.data.get('id_hackaton')

        serializer = HackatonUserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(status=200, data={'result':'success'})

@extend_schema(tags=["Team Views"])
class TeamView(APIView):
    permission_classes = [IsAuthenticated,]
    #получить по id
    @extend_schema(
        description='Получение команды по id',
        parameters=[OpenApiParameter(name='team', description='id team', required=True, type=int),],
        responses={200: OpenApiTypes.OBJECT, 404: OpenApiTypes.OBJECT},
        examples=[OpenApiExample(name='Example get team', value={"result": {
                    "list_team": [{"id_hackaton_user": 2, "first_name": "admin", "last_name": "admin", "email": "b@mail.ru"}],
                    "team": {"id": 4, "title": "test", "description": "test", "hackaton": 1, "owner": 2}}}, 
                    response_only=True, status_codes=[200]),
                  OpenApiExample(name='Example get team', value={'error': 'message'}, response_only=True, status_codes=[404]),
        ],
    )
    def get(self, request):
        response = GetTeam().get_team(request.GET)
        return response

    #создать команду
    @extend_schema(
        description='Создать команду',
        request=OpenApiRequest(),
        responses={200: OpenApiTypes.OBJECT, 404: OpenApiTypes.OBJECT},
        examples=[OpenApiExample(name='Example create team', value={'result': 'заебца'}, response_only=True, status_codes=[200]),
                  OpenApiExample(name='Example create team', value={'error': 'message'}, response_only=True, status_codes=[404]),
                  OpenApiExample(name='Example create team', value={'id_hackaton': '1', 'title':'test_title', 'description':'test'}, request_only=True),
        ],
    )
    def post(self, request):
        response = GetTeam().create_team(user=request.user, data=request.data)
        return response


#получение списка своей команды по id хакатона
class MyTeamListView(APIView):
    permission_classes = [IsAuthenticated,]
    @extend_schema(
        tags=["Team Views"],
        description='Получение своей команды по id хакатона',
        parameters=[OpenApiParameter(name='id_hackaton', description='id хакатона', required=True, type=int),],
        responses={200: OpenApiTypes.OBJECT, 404: OpenApiTypes.OBJECT},
        examples=[OpenApiExample(name='Example get team', value={"result": {
                    "list_team": [{"id_hackaton_user": 2, "first_name": "admin", "last_name": "admin", "email": "b@mail.ru"}],
                    "team": {"id": 4, "title": "test", "description": "test", "hackaton": 1, "owner": 2}}}, 
                    response_only=True, status_codes=[200]),
                  OpenApiExample(name='Example get team', value={'error': 'message'}, response_only=True, status_codes=[404]),
        ],
    )
    def get(self, request):
        response = GetTeam().get_my_team(user=request.user.pk, data=request.GET)
        return response
        

#Приглашение в команду
@extend_schema(tags=['Invite in team'])
class InviteTeamView(APIView):
    permission_classes = [IsAuthenticated,]

    #дать инвайт
    @extend_schema(
        description='Пригласить в команду',
        request=OpenApiRequest(),
        responses={200: OpenApiTypes.OBJECT, 404: OpenApiTypes.OBJECT},
        examples=[OpenApiExample(name='Example create invite', value={'result': 'заебца'}, response_only=True, status_codes=[200]),
                  OpenApiExample(name='Example create invite', value={'error': 'message'}, response_only=True, status_codes=[404]),
                  OpenApiExample(name='Example create invite', description='Нужен id стандартного юзера', value={'id_hackaton': '1', 'user':'1'}, request_only=True),
        ],
    )
    def post(self, request):
        response = GetUserTeam().create_invite(user=request.user, data=request.data)
        return response
    
    #принять инвайт 
    @extend_schema(
        description='Принять инвайт в команду',
        request=OpenApiRequest(),
        responses={200: OpenApiTypes.OBJECT, 404: OpenApiTypes.OBJECT},
        examples=[OpenApiExample(name='Example accept invite', value={'result': 'заебца'}, response_only=True, status_codes=[200]),
                  OpenApiExample(name='Example accept invite', value={'error': 'message'}, response_only=True, status_codes=[404]),
                  OpenApiExample(name='Example accept invite', description='', value={'team': '1'}, request_only=True),
        ],
    )
    def patch(self, request):
        response = GetUserTeam().accept_invite(user=request.user, data=request.data)
        return response
    
    #Выйти из команды
    @extend_schema(
        description='Выйти из команды',
        request=OpenApiRequest(),
        responses={200: OpenApiTypes.OBJECT, 404: OpenApiTypes.OBJECT},
        examples=[OpenApiExample(name='Example leave team', value={'result': 'заебца'}, response_only=True, status_codes=[200]),
                  OpenApiExample(name='Example leave team', value={'error': 'message'}, response_only=True, status_codes=[404]),
                  OpenApiExample(name='Example leave team', description='', value={'id_hackaton': '1'}, request_only=True),
        ],
    )
    def put(self, request):
        DeleteUserTeam().leave_from_team(request.user.pk, 
                            request.data.get('id_hackaton'))
        return Response(status=200, data={'result':'success'})

@extend_schema(tags=['Kick from team'])
class KickUserView(APIView):
    permission_classes = [IsAuthenticated,]

    #Удалить юзера из команды
    @extend_schema(
        description='Кикнуть из команды',
        parameters=[OpenApiParameter(name='id_hackaton', description='id хакатона', required=True, type=int),
                    OpenApiParameter(name='user', description='id user', required=True, type=int),],
        request=OpenApiRequest(),
        responses={200: OpenApiTypes.OBJECT, 404: OpenApiTypes.OBJECT},
        examples=[OpenApiExample(name='Example kick from team', value={'result': 'заебца'}, response_only=True, status_codes=[200]),
                  OpenApiExample(name='Example kick from team', value={'error': 'message'}, response_only=True, status_codes=[404]),
        ],
    )
    def delete(self, request):
        response = DeleteUserTeam().kick_user(user=request.GET.get('user'), 
                         id_hackaton=request.GET.get('id_hackaton'), 
                         owner=request.user.pk)  
        return response   


#получение хакатонов по заданным фильтрам
@extend_schema(
        tags=["Hackaton Views"],
        description='Получение списка хакатонов по заданным фильтрам',
        parameters=[OpenApiParameter(name='id', description='id хакатона', required=False, type=int),
                    OpenApiParameter(name='title', description='название хакатона', required=False, type=str),
                    OpenApiParameter(name='isOnline', description='онлайн', required=False, type=str),],
        responses={200: HackatonSerializer, 404: OpenApiTypes.OBJECT},
        examples=[OpenApiExample(name='Example get team', value={'error': 'message'}, response_only=True, status_codes=[404]),],
    )
class HackatonListView(generics.GenericAPIView, 
                      mixins.CreateModelMixin, 
                      mixins.ListModelMixin):
    permission_classes = [AllowAny,]
    serializer_class = HackatonSerializer

    def get_queryset(self):
        queryset = Hackaton.objects.all()
        filter = {}
        for i in self.request.GET.keys():
            filter[i] = self.request.GET[i]
        return queryset.filter(**filter)
    

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

@extend_schema(
        tags=["Hackaton Views"],
        description='Создание хакатона',
        request=HackatonSerializer,
        responses={200: OpenApiTypes.OBJECT, 404: OpenApiTypes.OBJECT},
        examples=[OpenApiExample(name='Example  create hackaton', value={'result': 'заебца'}, response_only=True, status_codes=[200]),
                  OpenApiExample(name='Example  create hackaton', value={'error': 'message'}, response_only=True, status_codes=[404]),],

    )
class HackatonCreateView(generics.GenericAPIView, 
                         mixins.CreateModelMixin):
    permission_classes = [IsAuthenticated,]
    serializer_class = HackatonSerializer

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)
    

@extend_schema(tags=['Invite in team'])
class HackatonUrlInvite(APIView):
    permission_classes = [IsAuthenticated,]

    @extend_schema(
        description='Создать ссылку инвайт',
        request=OpenApiRequest(),
        responses={200: OpenApiTypes.OBJECT, 404: OpenApiTypes.OBJECT},
        examples=[OpenApiExample(name='Example create url-invite', value={'result': 'url'}, response_only=True, status_codes=[200]),
                  OpenApiExample(name='Example create url-invite', value={'error': 'message'}, response_only=True, status_codes=[404]),
                  OpenApiExample(name='Example create url-invite', description='', value={'id_hackaton': '1'}, request_only=True),
        ],
    )
    def post(self, request):
        response = GetUserTeam().create_invite_url(user=request.user, data=request.data)
        return response
    
    @extend_schema(
        description='Принять инвайт по ссылке',
        request=OpenApiRequest(),
        responses={200: OpenApiTypes.OBJECT, 404: OpenApiTypes.OBJECT},
        examples=[OpenApiExample(name='Example accept url-invite', value={'result': 'заебца'}, response_only=True, status_codes=[200]),
                  OpenApiExample(name='Example accept url-invite', value={'error': 'message'}, response_only=True, status_codes=[404]),
        ],
    )
    def get(self, request):
        response = GetUserTeam().accept_url_invite(user=request.user, key=request.GET.get('team'))
        return response

