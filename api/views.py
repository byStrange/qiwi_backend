from django.shortcuts import render

from rest_framework import generics
from main.models import BasicUser
from .serializers import BasicUserSerializer

# Create your views here.

class UsersList(generics.ListCreateAPIView):
    queryset = BasicUser.objects.all()
    serializer_class = BasicUserSerializer
    