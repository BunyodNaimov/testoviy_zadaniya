from django.contrib.auth import authenticate
from django.shortcuts import render
from rest_framework import status, permissions
from rest_framework.generics import CreateAPIView, GenericAPIView
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken, Token

from users.models import CustomUser
from users.serializers import UserRegisterSerializer, UserLoginSerializer


class UserRegisterAPIView(CreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = UserRegisterSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        # parolni shifrlash
        user.set_password(request.data.get('password'))
        user.save()

        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class UserLoginAPIView(GenericAPIView):
    permission_classes = [permissions.AllowAny]
    serializer_class = UserLoginSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        username = serializer.validated_data.get('username')
        password = serializer.validated_data.get('password')
        user = authenticate(username=username, password=password)
        token = RefreshToken.for_user(user)
        data = serializer.data
        data['tokens'] = {'refresh': str(token), 'access': str(token.access_token)}
        return Response(data=data, status=status.HTTP_200_OK)
