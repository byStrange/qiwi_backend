from django.contrib.auth.models import User
from django.db import IntegrityError
from rest_framework.exceptions import ValidationError

from rest_framework import serializers

from main.models import (
    BasicUser,
    CityGroups,
    City,
    Category,
    Post,
    Image,
    Location,
    AD,
    Comment,
)

from chat.models import ChatMessage, Thread


class ADSerializer(serializers.ModelSerializer):
    class Meta:
        model = AD
        fields = "__all__"


class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        fields = "__all__"


class CitySerializer(serializers.ModelSerializer):
    class Meta:
        model = City
        fields = "__all__"


class RegionsSerializer(serializers.ModelSerializer):
    cities = CitySerializer(many=True)

    class Meta:
        model = CityGroups
        fields = "__all__"


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ("username", "password", "first_name")

    def create(self, validated_data):
        user = User.objects.create(
            username=validated_data["username"], first_name=validated_data["first_name"]
        )
        print(user)
        print(validated_data)
        user.set_password(validated_data["password"])
        user.save()
        return user


class CommentSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField()

    class Meta:
        model = Comment
        fields = "__all__"

    def get_user(self, obj):
        serializer = BasicUserSerializer(obj.user)
        return serializer.data


class BasicUserSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    location = LocationSerializer(required=False, read_only=True)
    comments = CommentSerializer(many=True, required=False, read_only=True)

    class Meta:
        model = BasicUser
        fields = (
            "id",
            "user",
            "city",
            "phone_number",
            "profile_img",
            "location",
            "comments",
            "top_attempts",
        )

    def create(self, validated_data):
        user_data = self.initial_data
        try:
            user = User.objects.create(
                username=user_data["user.username"],
                first_name=user_data["user.first_name"],
            )
        except IntegrityError:
            raise ValidationError("IntegrityError: Username already exists")
        user.set_password(user_data["user.password"])
        user.save()
        location = Location(
            latitude=user_data["location.lat"], longitude=user_data["location.lng"]
        )
        location.save()
        print(location)
        print(user.password)
        basic_user = BasicUser.objects.create(
            user=user, location=location, **validated_data
        )
        return basic_user


class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = "__all__"


class ThreadSerializer(serializers.ModelSerializer):
    first_person = BasicUserSerializer
    second_person = BasicUserSerializer

    class Meta:
        model = Thread
        fields = "__all__"


class ChatMessageSerializer(serializers.ModelSerializer):
    thread = ThreadSerializer
    attached_images = ImageSerializer(many=True)
    location = LocationSerializer()

    class Meta:
        model = ChatMessage
        fields = "__all__"


class AuthSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()

    def validate(self, data):
        user = User.objects.get(username=data["username"])
        if user.check_password(data["password"]):
            print("password is correct")
            data["user"] = user
        else:
            print("password is incorrect")
        return data


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = "__all__"


class PostSerializer(serializers.ModelSerializer):
    post_type = CategorySerializer(read_only=True)
    user = BasicUserSerializer(
        read_only=True,
        default=serializers.CurrentUserDefault(),
    )
    city = CitySerializer(read_only=True)
    images = serializers.SerializerMethodField()
    location = LocationSerializer(read_only=True, required=False)

    class Meta:
        model = Post
        fields = "__all__"

    def get_images(self, post):
        image_urls = []
        for image in post.images.all():
            image_urls.append({"id": image.id, "image": image.image.url})
        return image_urls


class WritePostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = "__all__"
