from rest_framework import serializers

from users.models import CustomUser


class UserRegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ('id', 'username', 'password')


class UserLoginSerializer(serializers.ModelSerializer):
    username = serializers.CharField(max_length=100)
    password = serializers.CharField(max_length=100)

    class Meta:
        model = CustomUser
        fields = ('username', 'password')
