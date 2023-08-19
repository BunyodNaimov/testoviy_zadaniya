from django.urls import path

from users.views import UserRegisterAPIView, UserLoginAPIView, SendPhoneVerificationCodeView

app_name = 'users'
urlpatterns = [
    path('register/', UserRegisterAPIView.as_view(), name='user-register'),
    path('login/', UserLoginAPIView.as_view(), name='user-login'),
    path('send-phone-verification-code', SendPhoneVerificationCodeView.as_view(), name='send-code')
]