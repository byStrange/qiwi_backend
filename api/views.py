from django.contrib.auth.models import User
from django.contrib.sessions.backends.db import SessionStore
from rest_framework import generics
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import BasicUserSerializer, RegionsSerializer
from main.models import BasicUser, CityGroups, City

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

class SetCityView(APIView):
    def get(self, request):
        city_id = request.GET.get('city')
        if city_id:
            session = SessionStore()
            session['city_id'] = city_id
            session.save()

            return Response({"success": True})
        return Response({"success": False, "status": "City id was not provided"})
    
class UserRegistrationView(APIView):
    def post(self, request, format=None):
        phone_number = request.data.get("phone_number")
        confirmation_code = request.data.get("confirmation_code")
        
        confirmed = True
        # verifiy confirmation code
        
        if confirmed:
            city_id = request.session.get('city_id')
            try: 
                city = City.objects.get(pk=city_id)
            except City.DoesNotExist:
                return Response({"error": "Invalid city ID"}, status=status.HTTP_400_BAD_REQUEST)
            
            user = User.objects.create_user(username=str(phone_number))
            basic_user = BasicUser(user=user, city=city, phone_number=phone_number)
            basic_user.save()

            return Response({"success": True},  status=status.HTTP_201_CREATED)