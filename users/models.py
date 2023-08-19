from datetime import timedelta

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _
from rest_framework_simplejwt.tokens import RefreshToken

from users.manager import UserManager
from users.utils import phone_regex


class User(AbstractUser):
    username = models.CharField(max_length=150, unique=True, null=True, blank=True)
    phone_number = models.CharField(
        validators=[phone_regex],
        max_length=15,
        unique=True,
        error_messages={
            "unique": _("A user with that phone number already exists."),
        },
    )

    profile_picture = models.ImageField(upload_to="profile_pictures", null=True, blank=True)
    birth_date = models.DateField(null=True, blank=True)

    USERNAME_FIELD = "phone_number"

    objects = UserManager()

    def __str__(self):
        return self.phone_number

    @property
    def full_name(self):
        return "{} {}".format(self.first_name, self.last_name).strip()

    def tokens(self):
        refresh = RefreshToken.for_user(self)
        return {"access": str(refresh.access_token), "refresh": str(refresh)}


class VerificationCode(models.Model):
    class VerificationTypes(models.TextChoices):
        REGISTER = "register"
        LOGIN = "login"

    code = models.CharField(max_length=6)
    user = models.ForeignKey(
        "users.User", on_delete=models.CASCADE, related_name="verification_codes", null=True, blank=True
    )
    phone = models.CharField(max_length=15, unique=True, null=True, validators=[phone_regex])
    verification_type = models.CharField(max_length=50, choices=VerificationTypes.choices)
    last_sent_time = models.DateTimeField(auto_now=True)
    is_verified = models.BooleanField(default=False)
    expired_at = models.DateTimeField(null=True)

    def __str__(self):
        return self.phone

    class Meta:
        unique_together = ["phone", "verification_type"]

    @property
    def is_expire(self):
        return self.expired_at < self.last_sent_time + timedelta(seconds=30)
