from django.contrib.auth.models import User
from rest_framework import serializers


from main.models import BasicUser, CityGroups, City


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
    confirm_password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ('username', 'email', 'password', 'confirm_password')

    def create(self, validated_data):
        user = User.objects.create(
            username=validated_data['username'],
            email=validated_data['email']
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
        password = user_data.pop('password')
        confirm_password = user_data.pop('confirm_password')
        if password != confirm_password:
            raise serializers.ValidationError("Passwords do not match")
        user = User.objects.create_user(password=password, **user_data)
        basic_user = BasicUser.objects.create(user=user, **validated_data)
        return basic_user