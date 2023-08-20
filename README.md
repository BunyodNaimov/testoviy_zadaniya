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
