from django.core.validators import RegexValidator


phone_regex = RegexValidator(
    regex=r"^\+?1?\d{9,15}$",
    message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.",
)

DEFAULT_DIAL_CODE = "+998"


# def check_verification_code(phone_number, verification_type, code):
#     verification_code = VerificationCode.objects.filter(phone=phone_number, verification_type=verification_type,
#                                                         is_verified=False).last()
#
#     if verification_code:
#         if not verification_code.expired and verification_code.code == code:
#             verification_code.is_verified = True
#             verification_code.save(update_fields=['is_verified'])
#             return True
#         return False


