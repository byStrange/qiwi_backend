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

