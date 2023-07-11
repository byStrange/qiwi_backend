from django.shortcuts import get_object_or_404
from django.contrib.auth import login
from django.views.decorators.csrf import csrf_exempt
from django.http import Http404
from django.db.models import Max, OuterRef, Subquery

from rest_framework import generics
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.authtoken.serializers import AuthTokenSerializer
from rest_framework.exceptions import ValidationError


from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync

from knox.models import AuthToken
from knox.views import LoginView as KnoxLoginView

import json

from main.models import BasicUser, CityGroups, Post, Category, AD, City, Location, Image
from chat.models import ChatMessage, Thread
from chat.models import Thread, ChatMessage

from .serializers import (
    BasicUserSerializer,
    RegionsSerializer,
    UserSerializer,
    PostSerializer,
    AuthSerializer,
    CategorySerializer,
    ADSerializer,
    WritePostSerializer,
    ChatMessageSerializer,
    ThreadSerializer,
    LocationSerializer,
)


class ProfileView(APIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = BasicUserSerializer

    def get(self, request):
        user = request.user
        basic_user = BasicUser.objects.get(user=user)
        return Response({"user": self.serializer_class(basic_user).data})

    def patch(self, request):
        user = request.user
        basic_user = BasicUser.objects.get(user=user)
        first_name = request.data.get("user.first_name")
        location = request.data.get("location")
        print(location)
        if location:
            lat = location.get("latitude")
            lng = location.get("longitude")
            if basic_user.location:
                basic_user.location.latitude = lat
                basic_user.location.longitude = lng
            else:
                location = Location(latitude=lat, longitude=lng)
                location.save()
                basic_user.location = location
            basic_user.save()
        if first_name:
            user.first_name = first_name
            user.save()
        serializer = self.serializer_class(basic_user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UsersList(generics.ListCreateAPIView):
    queryset = BasicUser.objects.all()
    serializer_class = BasicUserSerializer


class UserDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = BasicUser.objects.all()
    serializer_class = BasicUserSerializer


class ADsList(generics.ListCreateAPIView):
    queryset = AD.objects.all()
    serializer_class = ADSerializer


class RegionsList(generics.ListCreateAPIView):
    queryset = CityGroups.objects.all()
    serializer_class = RegionsSerializer


class Region(generics.RetrieveUpdateDestroyAPIView):
    queryset = CityGroups.objects.all()
    serializer_class = RegionsSerializer


class LoginView(KnoxLoginView):
    # login view extending KnoxLoginView
    serializer_class = AuthSerializer
    permission_classes = (AllowAny,)

    def post(self, request, format=None):
        serializer = AuthTokenSerializer(
            data=request.data, context={"request": request}
        )
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data["user"]
        print(user)
        login(request, user)
        return super(LoginView, self).post(request, format=None)


class CheckAuthView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        return Response({"isAuthenticated": True, "username": request.user.username})


class RegisterView(APIView):
    serializer_class = BasicUserSerializer

    def post(self, request, format=None):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        basic_user = serializer.save()
        # raise ValidationError("409: USERNAME ALREADY EXISTS")
        user = basic_user.user

        _, token = AuthToken.objects.create(user)
        return Response(
            {"user": UserSerializer(user).data, "token": token},
            status=status.HTTP_201_CREATED,
        )


class PostView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        basic_user = BasicUser.objects.get(user=request.user)
        images_data = request.data.pop("images", [])

        images = []

        for image_data in images_data:
            image = Image.objects.create(image=image_data)
            images.append(image)

        # get ids
        city_id = request.data.get("city")
        post_type_id = request.data.get("post_type")
        location_id = request.data.get("location")
        is_top = request.data.get("top")
        location = None
        if location_id:
            location = Location.objects.get(id=location_id)

        # get objects
        city = City.objects.get(id=city_id)
        post_type = Category.objects.get(id=post_type_id)
        # location = Location.objects.get(id=location_id)
        if is_top:
            basic_user.top_attempts -= 1
            basic_user.save()
        serializer = PostSerializer(data=request.data, context={"request": request})

        if serializer.is_valid():
            serializer.save(
                user=basic_user,
                city=city,
                post_type=post_type,
                location=location,
                images=images,
            )
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request):
        posts = Post.objects.order_by("-updated_at")
        city_id = request.query_params.get("city")
        if city_id:
            posts = posts.filter(city__id=city_id)
        serializer = PostSerializer(posts, many=True)
        return Response(serializer.data)


class GenerateImages(APIView):
    def post(self, request):
        img_files = request.FILES.getlist("images", [])
        images = []
        for img_file in img_files:
            image = Image.objects.create(image=img_file)
            images.append({"id": image.id, "image": image.image.url})
        return Response({"images": images})


class GenerateLocation(APIView):
    serializer_class = LocationSerializer

    def post(self, request):
        data = request.data
        location = Location.objects.create(
            latitude=data["location"]["lat"], longitude=data["location"]["lng"]
        )
        serialized = self.serializer_class(location)
        return Response(serialized.data)


class PostDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Post.objects.all()
    permission_classes = (IsAuthenticated,)

    def get_serializer_class(self):
        if self.request.method == "GET":
            return PostSerializer
        return WritePostSerializer


class PostLikeView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request, pk):
        post = get_object_or_404(Post, pk=pk)
        user = BasicUser.objects.get(user=request.user)
        if post.has_user_liked(user):
            post.remove_like(user)
            return Response(
                {"success": True, "message": "disliked"}, status=status.HTTP_200_OK
            )
        else:
            post.increase_likes(user)
            return Response(
                {"success": True, "message": "liked"}, status=status.HTTP_200_OK
            )


class PostViewView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request, pk):
        post = get_object_or_404(Post, pk=pk)
        user = BasicUser.objects.get(user=request.user)
        if post.has_user_viewed(user):
            return Response(
                {"message": "User has already viewed this post"},
            )
        else:
            post.increase_views(user)
            return Response(status=status.HTTP_200_OK)


class CategoriesView(generics.ListCreateAPIView):
    serializer_class = CategorySerializer
    queryset = Category.objects.all()


class ThreadView(generics.ListCreateAPIView):
    serializer_class = ThreadSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        user = BasicUser.objects.get(user=self.request.user)
    
        # Get the maximum timestamp for each thread
        subquery = ChatMessage.objects.filter(thread=OuterRef("id")).values("thread").annotate(
                max_timestamp=Max("timestamp")
        ).values("max_timestamp")

        # Order the threads based on the maximum timestamp
        queryset = Thread.objects.annotate(
            last_message_timestamp=Subquery(subquery)
        ).filter(members=user).order_by("-last_message_timestamp")
        return queryset

class ThreadChatMessagesAPIView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, uuid):
        try:
            thread = Thread.objects.get(id=uuid)
        except Thread.DoesNotExist:
            return Response(
                {"error": "Thread not found"}, status=status.HTTP_404_NOT_FOUND
            )
        user = BasicUser.objects.get(user=request.user)
        if not thread.members.filter(id=user.id).exists():
            return Response(
                {
                    "error": "User is not a member of the thread",
                },
                status=status.HTTP_403_FORBIDDEN,
            )
        chat_messages = ChatMessage.objects.filter(thread=thread)
        serializer = ChatMessageSerializer(chat_messages, many=True)
        return Response(serializer.data)


class DeleteMessagesView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        # Get the necessary data from the request
        thread_id = request.data.get("thread_id")
        message_ids = request.data.get("message_ids")
        user = BasicUser.objects.get(user=request.user)
        user_id = user.id

        # Validate the data
        if not thread_id or not message_ids:
            return Response(
                {"error": "Missing required data"}, status=status.HTTP_400_BAD_REQUEST
            )

        try:
            # Ensure the thread exists
            thread = Thread.objects.get(id=thread_id)

            # Check if the user is a member of the thread
            if not thread.members.filter(id=user_id).exists():
                return Response(
                    {"error": "User is not a member of the thread"},
                    status=status.HTTP_403_FORBIDDEN,
                )

            # Delete the messages associated with the thread and message IDs
            ChatMessage.objects.filter(thread=thread, id__in=message_ids).delete()
            channel_layer = get_channel_layer()
            async_to_sync(channel_layer.group_send)(
                f"chat_{thread_id}",
                {
                    "type": "chat_message",
                    "message": json.dumps(
                        {
                            "action": "deleteMessages",
                            "thread_id": thread_id,
                            "message_ids": message_ids,
                        }
                    ),
                },
            )
            return Response(
                {"success": "Messages deleted successfully"}, status=status.HTTP_200_OK
            )

        # There is no thread with this id
        except Thread.DoesNotExist:
            return Response(
                {"error": "Thread not found"}, status=status.HTTP_404_NOT_FOUND
            )

        # There was a problem deleting a message
        except Exception as e:
            return Response(
                {"error": "Failed to delete messages"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )


class ReadMessagesView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        # Get the necessary data from the request
        thread_id = request.data.get("thread_id")
        message_ids = request.data.get("message_ids")
        user = BasicUser.objects.get(user=request.user)
        user_id = user.id

        # Validate the data
        if not thread_id or not message_ids:
            return Response(
                {"error": "Missing required data"}, status=status.HTTP_400_BAD_REQUEST
            )

        try:
            # Ensure the thread exists
            thread = Thread.objects.get(id=thread_id)

            # Check if the user is a member of the thread
            if not thread.members.filter(id=user_id).exists():
                return Response(
                    {"error": "User is not a member of the thread"},
                    status=status.HTTP_403_FORBIDDEN,
                )

            # Delete the messages associated with the thread and message IDs
            messages = ChatMessage.objects.filter(thread=thread, id__in=message_ids)
            for message in messages:
                if message.user.id != user_id:
                    message.read = True
                    message.save()

            channel_layer = get_channel_layer()
            async_to_sync(channel_layer.group_send)(
                f"chat_{thread_id}",
                {
                    "type": "chat_message",
                    "message": json.dumps(
                        {
                            "action": "readMessages",
                            "thread_id": thread_id,
                            "message_ids": message_ids,
                        }
                    ),
                },
            )
            return Response(
                {"success": "Messages read successfully"}, status=status.HTTP_200_OK
            )

        # There is no thread with this id
        except Thread.DoesNotExist:
            return Response(
                {"error": "Thread not found"}, status=status.HTTP_404_NOT_FOUND
            )

        # There was a problem deleting a message
        except Exception as e:
            return Response(
                {"error": "Failed to delete messages"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

class DeleteThreadView(APIView):
    def post(self, request, uuid):
        try:
            thread = get_object_or_404(Thread, id=uuid)
            # Perform the deletion logic here...
            thread.delete()
            return Response({'success': True})
        except Http404:
            return Response({'success': False}, status=404)
        
