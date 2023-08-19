import random
import string
from django.utils.crypto import get_random_string
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

from users.models import User
from users.send_code import send_code_to_phone
from users.serializers import (
    SendPhoneVerificationCodeSerializer,
    CheckPhoneVerificationCodeSerializer,
    UserProfileSerializer, UserSerializer)
from users.models import VerificationCode


class SendPhoneVerificationCodeView(APIView):

    @swagger_auto_schema(request_body=SendPhoneVerificationCodeSerializer)
    def post(self, request, *args, **kwargs):
        serializer = SendPhoneVerificationCodeSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        phone = serializer.validated_data.get("phone")
        code = get_random_string(allowed_chars="0123456789", length=4)
        verification_code, _ = (
            VerificationCode.objects.update_or_create(
                phone=phone, defaults={"code": code, "is_verified": False}
            )
        )
        # response_from_service = send_code_to_phone(phone, code)
        return Response({"detail": "response_from_service"})


class CheckPhoneVerificationCodeView(CreateAPIView):
    queryset = VerificationCode.objects.all()
    serializer_class = CheckPhoneVerificationCodeSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        phone = serializer.validated_data.get("phone")
        code = serializer.validated_data.get("code")

        try:
            send_code = VerificationCode.objects.filter(phone=phone, is_verified=True).first().code

        except:
            pass
        else:
            if send_code != code:
                raise ValidationError("Verification code invalid.")

        verification_code = (
            self.get_queryset().filter(phone=phone, is_verified=False).order_by("-last_sent_time").first()
        )
        if verification_code and verification_code.code != code:
            raise ValidationError("Verification code invalid.")

        if verification_code is None:
            raise ValidationError("Verification code active.")

        verification_code.is_verified = True
        verification_code.save(update_fields=["is_verified"])

        # Проверка, если пользователь ранее не авторизовывался
        user = User.objects.filter(phone_number=phone).first()
        if not user:
            invite_code = ''
            # Генерация случайного инвайт-кода
            while True:
                invite_code = ''.join(random.choices(string.ascii_letters + string.digits, k=6))
                if invite_code.isalnum():
                    break
            # Создание нового пользователя с инвайт-кодом
            user = User.objects.create_user(phone_number=phone, invite_code=invite_code.upper())
        return Response({"tokens": user.tokens(), "detail": "Verification code is verified."})


class ProfileAPIView(APIView):
    permission_classes = [IsAuthenticated]

    # def get(self, request, *args, **kwargs):
    #     serializer = UserSerializer(request.user)
    #     return Response(serializer.data)

    # @swagger_auto_schema(request_body=UserSerializer)
    # def put(self, request, *args, **kwargs):
    #     serializer = UserSerializer(instance=request.user, data=request.data, partial=True)
    #     if serializer.is_valid():
    #         serializer.save()
    #         return Response(serializer.data)
    #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request, *args, **kwargs):
        user = request.user
        serializer = UserSerializer(user)
        return Response(serializer.data)

    @swagger_auto_schema(request_body=UserProfileSerializer)
    def post(self, request, *args, **kwargs):
        user = request.user
        invite_code = request.data.get("invite_code")
        print(user.invite_code)

        if user.invite_code_activated:
            return Response({"invite_code": user.invite_code}, status=200)

        # Проверка введенного инвайт-кода
        if  invite_code != user.invite_code and user.invite_code is not None:
            return Response({"detail": "Invalid invite code."}, status=400)

        # Проверка, что инвайт-код еще не был активирован
        if user.invite_code_activated:
            return Response({"detail": "Invite code has already been activated."}, status=400)

        # Присвоение статуса активации инвайт-кода пользователю
        user.invite_code_activated = True
        user.invite_code = invite_code
        user.save()
        # Дополнительная логика для активации инвайт-кода
        user.profile.is_completed = True
        user.profile.save()
        serializer = UserProfileSerializer(user)
        return Response(serializer.data)
