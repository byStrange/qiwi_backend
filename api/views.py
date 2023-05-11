from django.contrib.auth.models import User
from django.contrib.sessions.backends.db import SessionStore
from django.shortcuts import get_object_or_404

from rest_framework import generics
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from knox.models import AuthToken

from main.models import BasicUser, CityGroups, Post
from .serializers import BasicUserSerializer, RegionsSerializer, UserSerializer, PostSerializer

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
    serializer_class = BasicUserSerializer

    def post(self, request, format=None):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        basic_user = serializer.save()
        user = basic_user.user
        _, token = AuthToken.objects.create(user)
        return Response({
            "user":  UserSerializer(user).data,
            "token": token
        }, status=status.HTTP_201_CREATED)
    

class PostView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        serializer = PostSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def get(self, request):
        posts = Post.objects.all()
        serializer = PostSerializer(posts, many=True)
        return Response(serializer.data)
    

class PostDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = (IsAuthenticated,)


class PostLikeView(APIView):
    permission_classes = (IsAuthenticated,)
    
    def post(self, request, pk):
        post = get_object_or_404(Post, pk=pk)
        user = BasicUser(user=request.user)
        if post.has_user_liked(user):
            return Response({"message": "User has already liked this post"})
        else:
            post.increase_likes(user)
            return Response(status=status.HTTP_200_OK)
        

class PostViewView(APIView):
    permission_classes = (IsAuthenticated, )

    def post(self, request, pk):
        post = get_object_or_404(Post, pk=pk)
        user = BasicUser(user=request.user)
        if post.has_user_viewed(user):
            return Response({"message": "User has already viewed this post"})
        else:
            post.increase_views(user)
            return Response(status=status.HTTP_200_OK)
        
