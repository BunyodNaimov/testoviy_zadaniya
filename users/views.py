import random
import string
from django.utils.crypto import get_random_string
from drf_yasg.utils import swagger_auto_schema
from rest_framework.exceptions import ValidationError
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

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
        response_from_service = send_code_to_phone(phone, code)
        return Response({"detail": response_from_service})


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
            invite_code_own = ''
            # Генерация случайного инвайт-кода
            while True:
                invite_code_own = ''.join(random.choices(string.ascii_letters + string.digits, k=6))
                if invite_code_own.isalnum():
                    break
            # Создание нового пользователя с инвайт-кодом
            user = User.objects.create_user(phone_number=phone, invite_code_own=invite_code_own.upper())
        return Response({"tokens": user.tokens(), "detail": "Verification code is verified."})


class ProfileAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        user = request.user
        serializer = UserProfileSerializer(user)
        return Response(serializer.data)

    @swagger_auto_schema(request_body=UserSerializer)
    def post(self, request, *args, **kwargs):
        user = request.user
        invite_code = request.data.get("invite_code")
        if invite_code == user.invite_code_own:
            return Response({"detail": "Invalid invite code."}, status=400)

        if user.invite_code_used_activated:
            return Response({"detail": "Invite code has already been activated."}, status=400)

        user.invite_code_used_activated = True
        user.invite_code_used = invite_code
        user.save()
        serializer = UserProfileSerializer(user)
        return Response(serializer.data)
