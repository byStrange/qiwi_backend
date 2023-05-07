from django.contrib.auth.models import User
from rest_framework import serializers


from main.models import BasicUser, CityGroups, City, Category, Post


class BasicUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = BasicUser
        fields = '__all__'


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
        user = User.objects.create(**user_data)
        basic_user = BasicUser.objects.create(user=user, **validated_data)
        return basic_user
    
class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class PostSerializer(serializers.ModelSerializer):
    post_type = CategorySerializer(read_only=True)
    user = serializers.PrimaryKeyRelatedField(read_only=True, default=serializers.CurrentUserDefault())

    class Meta:
        model = Post
        fields = '__all__'