from django.contrib.auth.models import User
from django.contrib.auth.hashers import  make_password

from rest_framework import serializers

from main.models import BasicUser, CityGroups, City, Category, Post


class CitySerializer(serializers.ModelSerializer):
    class Meta:
        model = City
        fields = '__all__'


class RegionsSerializer(serializers.ModelSerializer):
    cities = CitySerializer(many=True)
    
    class Meta:
        model = CityGroups
        fields = '__all__'


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ('username', 'password')
    
    def create(self, validated_data):
        user = User.objects.create(
            username=validated_data['username'],
        )
        print("_________________________________________________________________________________---------------------------------------------------_______________________z")
        print(user)
        print(validated_data)
        user.set_password(validated_data['password'])
        user.save()
        return user


class BasicUserSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = BasicUser
        fields = ('user', 'city', 'phone_number', 'profile_img')

    def create(self, validated_data):
        user_data = validated_data.pop('user')
        user = User.objects.create(username=user_data['username'])
        password = make_password(user_data['password'])
        user.set_password(password)
        user.save()
        print(user.password)
        basic_user = BasicUser.objects.create(user=user, **validated_data)
        return basic_user


class AuthSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()

    def validate(self, data):
        print(data)
        user = User(username=data["username"])
        print(user)
        print(data['password'])
        if user.check_password(data['password']):
            data['user'] = user
        else:
            print("password is incorrect")  
        return data

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class PostSerializer(serializers.ModelSerializer):
    post_type = CategorySerializer(read_only=True)
    user = serializers.PrimaryKeyRelatedField(
        read_only=True,
        default=serializers.CurrentUserDefault(),
    )

    class Meta:
        model = Post
        fields = '__all__'
