from rest_framework import serializers

from users.models import User
from users.utils import phone_regex


class UserSerializer(serializers.ModelSerializer):
    invite_code_activated = serializers.BooleanField(read_only=True)
    invite_code = serializers.CharField(read_only=True)

    class Meta:
        model = User
        fields = (
            "id", "username", "invite_code", 'invite_code_activated', "email", "first_name", "last_name", "phone_number"
        )


class UserProfileSerializer(serializers.ModelSerializer):
    invite_code = serializers.CharField()

    class Meta:
        model = User
        fields = (
            "id", "invite_code",
        )


class SendPhoneVerificationCodeSerializer(serializers.Serializer):
    phone = serializers.CharField(max_length=15, validators=[phone_regex])


class CheckPhoneVerificationCodeSerializer(serializers.Serializer):
    phone = serializers.CharField(max_length=15, validators=[phone_regex])
    code = serializers.CharField(min_length=4, max_length=4)
