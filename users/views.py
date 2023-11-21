from django.shortcuts import render
from rest_framework.views import APIView
from .serializers import UserSerializer
from django.http import JsonResponse
from .queries import GetUser, UserScore
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticatedOrReadOnly, IsAuthenticated
from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiExample, OpenApiResponse, OpenApiRequest
from drf_spectacular.types import OpenApiTypes
from rest_framework import viewsets
from .models import User


@extend_schema(
        tags=["User Views"],
        description='CRUD user',
    )
class UserViewSet(viewsets.ModelViewSet):
    permission_classes = [AllowAny, ]
    queryset = User.objects.all()
    serializer_class = UserSerializer



