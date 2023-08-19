from django.contrib import admin

from users.models import User, VerificationCode

admin.site.register(User)


@admin.register(VerificationCode)
class VerificationCodeAdmin(admin.ModelAdmin):
    list_display = ["phone", "code", "last_sent_time", "expired_at", "is_verified"]
    ordering = ["-last_sent_time"]
