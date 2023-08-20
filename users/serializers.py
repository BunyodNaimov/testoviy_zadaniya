from rest_framework import serializers

from users.models import User
from users.utils import phone_regex


class UserProfileSerializer(serializers.ModelSerializer):
    invite_code_used_activated = serializers.BooleanField(read_only=True)
    invite_code_own = serializers.CharField(read_only=True)
    invite_code_used = serializers.CharField(read_only=True)
    invited_users = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = User
        fields = (
            "id", "username", "invited_users", "invite_code_own", "invite_code_used", 'invite_code_used_activated',
            "email", "first_name", "last_name", "phone_number"
        )

    def get_invited_users(self, obj):
        if obj.invite_code_used_activated:
            invited_users = User.objects.filter(invite_code_used=obj.invite_code_own)
            return invited_users.values_list('phone_number', flat=True)
        return []


class UserSerializer(serializers.ModelSerializer):
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
