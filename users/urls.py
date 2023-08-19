from django.urls import path

from users.views import SendPhoneVerificationCodeView, ProfileAPIView, CheckPhoneVerificationCodeView

app_name = 'users'
urlpatterns = [
    path('profile/', ProfileAPIView.as_view(), name='user-profile'),
    path('send-phone-verification-code', SendPhoneVerificationCodeView.as_view(), name='send-code'),
    path('check-phone-verification-code', CheckPhoneVerificationCodeView.as_view(), name='check-code'),
]
