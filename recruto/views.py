from django.contrib.auth import logout
from django.shortcuts import render

# Create your views here.

from django.http import HttpResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

import random

def task_1(request):
    code = random.randrange(1000, 9999, 1)
    return HttpResponse(f"Случайный четырехзначный код: {code}")



class task_2(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        code = random.randrange(1000, 9999, 1)
        logout(request)
        return Response({'Случайный четырехзначный код': code}, status=status.HTTP_200_OK)


