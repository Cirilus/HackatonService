from django.shortcuts import render
from rest_framework.views import APIView
from .serializers import UserSerializer
from django.http import JsonResponse
from .queries import GetUser, UserScore
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticatedOrReadOnly, IsAuthenticated


class UserView(APIView):

    @permission_classes([AllowAny,])
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return JsonResponse({'result':'success'})
    
    @permission_classes([IsAuthenticated,])
    def put(self, request):
        serializer = UserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return JsonResponse({'result':'success'})
    
    def delete(self, request):
        GetUser().delete_user(request.data.get('id_user'))
        return JsonResponse({'result':'success'})



