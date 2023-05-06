from django.contrib.auth.models import User 
from django.contrib.sessions.backends.db import SessionStore
from rest_framework import generics
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import BasicUserSerializer, RegionsSerializer, UserSerializer
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

# class UserRegistrationView(APIView):
#     def post(self, request, format=None):
#         phone_number = request.data.get("phone_number")
#         city_id = request.data.get("city_id")
#         confirmation_code = request.data.get("confirmation_code")
        
#         confirmed = True
#         # verifiy confirmation code
        
#         if confirmed:
#             try: 
#                 city = City.objects.get(pk=city_id)
#             except City.DoesNotExist:
#                 return Response({"error": "Invalid city ID"}, status=status.HTTP_400_BAD_REQUEST)

#             phone_number = phone_number.replace("+", "")
#             user = User.objects.create_user(username=str(phone_number))
#             basic_user = BasicUser(user=user, city=city, phone_number=phone_number)
#             basic_user.save()

#             return Response({"success": True},  status=status.HTTP_201_CREATED)

class RegisterView(APIView):
    def post(self, request):
        user_serializer = UserSerializer(data=request.data)
        if user_serializer.is_valid():
            user = user_serializer.save()
            basic_user_serializer = BasicUserSerializer(data=request.data)
            if basic_user_serializer.is_valid():
                basic_user = basic_user_serializer.save(user=user)
                return Response({
                    'user': user_serializer.data,
                    'basic_user': basic_user_serializer.data
                }, status=status.HTTP_201_CREATED)
        return Response(user_serializer.errors, status=status.HTTP_400_BAD_REQUEST)