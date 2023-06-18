from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    address = models.CharField(max_length=255, null=True)
    phone = models.CharField(max_length=15, null=True)
    dob = models.DateField(null=True)
    created_at = models.DateField(auto_now=True)
