from django.shortcuts import render
from rest_framework import generics
from .serializers import BasicUserSerializer, RegionsSerializer
from main.models import BasicUser, CityGroups

# Create your views here.

class UsersList(generics.ListCreateAPIView):
    queryset = BasicUser.objects.all()
    serializer_class = BasicUserSerializer


class RegionsList(generics.ListCreateAPIView):
    queryset = CityGroups.objects.all()
    serializer_class = RegionsSerializer


class Region(generics.RetrieveUpdateDestroyAPIView):
    queryset = CityGroups.objects.all()
    serializer_class = RegionsSerializer