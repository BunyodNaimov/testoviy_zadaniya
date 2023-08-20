## Добро пожаловать в проект [Тестовое задание для Python разработчика](https://testoviyzadaniya.pythonanywhere.com/swagger/)!
# Обзор проекта

Этот проект представляет простую реферальную систему с использованием Python, Django, Django REST Framework (DRF) и PostgreSQL.

# Установка

Чтобы запустить этот проект на своем локальном компьютере, выполните следующие шаги:

Установите Django, выполнив следующую команду:
```stylus
pip install django
```

Клонируйте репозиторий проекта:
```stylus
https://github.com/BunyodNaimov/testoviy_zadaniya.git
```

Перейдите в директорию проекта:
```stylus
cd minbar-uz-clone
```
Создайте виртуальное окружение:
```stylus
python -m venv env
```

Активируйте виртуальное окружение:
```stylus
source env/bin/activate
```
Установите необходимые пакеты:
```stylus
pip install -r requirements.txt
```

Запустите сервер:
```stylus
python manage.py runserver
```

Перейдите на веб-сайт по адресу ```stylus http://127.0.0.1:8000/``` в вашем браузере.

# Модели
## Модель пользователя (User)
Модель User представляет зарегистрированного пользователя в системе. Она наследуется от модели AbstractUser, предоставляемой Django, и включает следующие поля:
```stylus
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
    invite_code_own = models.CharField(unique=True, max_length=6, blank=True, null=True)
    invite_code_used = models.CharField(unique=True, max_length=6, blank=True, null=True)
    invite_code_used_activated = models.BooleanField(default=False)

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
```
Модель User также включает пользовательские методы и свойства:

`__str__()`: Возвращает номер телефона пользователя.

`full_name`: Свойство, возвращающее полное имя пользователя.

`tokens()`: Возвращает словарь, содержащий токены доступа и обновления с использованием RefreshToken из rest_framework_simplejwt.tokens.

# Модель верификационного кода (VerificationCode)
Модель VerificationCode представляет верификационный код, связанный с пользователем. Она включает следующие поля:
```style
class VerificationCode(models.Model):
    code = models.CharField(max_length=6)
    user = models.ForeignKey(
        "users.User", on_delete=models.CASCADE, related_name="verification_codes", null=True, blank=True
    )
    phone = models.CharField(max_length=15, unique=True, null=True, validators=[phone_regex])
    last_sent_time = models.DateTimeField(auto_now=True)
    is_verified = models.BooleanField(default=False)
    expired_at = models.DateTimeField(null=True)

    def __str__(self):
        return self.phone
```
# Представления (Views)
## SendPhoneVerificationCodeView (APIView)
```style
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
```
SendPhoneVerificationCodeView - представление для отправки кода верификации на указанный телефон. Оно наследуется от APIView и содержит метод post, который обрабатывает POST-запросы. В методе post используется SendPhoneVerificationCodeSerializer для валидации данных, после чего генерируется случайный код и отправляется на указанный телефон. Ответ возвращается в формате JSON с деталями результата отправки кода.

## CheckPhoneVerificationCodeView (CreateAPIView)
```style
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

        user = User.objects.filter(phone_number=phone).first()
        if not user:
            invite_code_own = ''
            while True:
                invite_code_own = ''.join(random.choices(string.ascii_letters + string.digits, k=6))
                if invite_code_own.isalnum():
                    break
            user = User.objects.create_user(phone_number=phone, invite_code_own=invite_code_own.upper())
        return Response({"tokens": user.tokens(), "detail": "Verification code is verified."})
```

CheckPhoneVerificationCodeView - представление для проверки верификационного кода, введенного пользователем. Оно наследуется от CreateAPIView и определяет метод create, который обрабатывает POST-запросы. В методе create используется CheckPhoneVerificationCodeSerializer для валидации данных, после чего происходит проверка верификационного кода. Если код верен, то устанавливается флаг верификации для соответствующего объекта VerificationCode, создается новый пользователь, если его нет в базе данных, и возвращается ответ с токенами доступа и деталями верификации.


## ProfileAPIView(APIView)
```style
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
```


ProfileAPIView - представление для работы с профилем пользователя. Оно наследуется от APIView и требует аутентификации (IsAuthenticated) для доступа. Представление содержит методы get и post. Метод get возвращает данные профиля аутентифицированного пользователя в формате JSON. Метод post обрабатывает POST-запросы для активации кода приглашения. Если код приглашения верен и еще не был активирован, то устанавливается флаг активации и возвращаются данные профиля.
