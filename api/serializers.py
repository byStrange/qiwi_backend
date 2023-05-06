from rest_framework import serializers

from main.models import BasicUser


class BasicUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = BasicUser
        fields = '__all__'