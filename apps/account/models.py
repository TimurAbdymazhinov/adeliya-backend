from django.contrib.auth.models import AbstractUser, UserManager
from django.db import models
from django.db.models import Q, UniqueConstraint

from core.constants import GENDER_TYPE, MALE
from core.utils import generate_filename


class CustomUserManager(UserManager):
    def _create_user(self, phone, password, **extra_fields):
        """
        Create and save a user with the given phone, and password.
        """
        if not phone:
            raise ValueError('The given username must be set')
        user = self.model(phone=phone, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, phone, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(phone, password, **extra_fields)

    def create_superuser(self, phone, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(phone, password, **extra_fields)


class User(AbstractUser):
    username = None
    phone = models.CharField(max_length=25, unique=True, verbose_name='Телефон')
    avatar = models.ImageField(
        upload_to=generate_filename, null=True, blank=True,
        verbose_name='Аватар',
    )
    tmp_phone = models.CharField(
        max_length=25, verbose_name='Временный телефон', null=True, blank=True,
    )
    birth_date = models.DateField(null=True, verbose_name='Дата рождения',)
    gender = models.CharField(
        choices=GENDER_TYPE, default=MALE, max_length=10, verbose_name='Пол',
    )
    city = models.ForeignKey(
        to='City', verbose_name='Город', null=True, on_delete=models.SET_NULL,
        related_name='users',
    )
    active_point = models.PositiveIntegerField(
        default=0, verbose_name='Активные баллы',
    )
    inactive_point = models.PositiveIntegerField(
        default=0, verbose_name='Неактивные баллы',
    )
    discount = models.CharField(
        max_length=20, verbose_name='Скидка',
    )
    qr_code = models.CharField(
        max_length=255, blank=True, null=True, verbose_name='QR-код',
    )
    qr_code_updated_at = models.DateTimeField(
        blank=True, null=True, verbose_name='QR-код обновлен в',
    )
    is_registration_finish = models.BooleanField(
        default=False, verbose_name='is_registration_finish',
    )
    confirmation_code = models.CharField(
        verbose_name='confirmation code', max_length=6, null=True, blank=True,
    )
    confirmation_date = models.DateTimeField(
        verbose_name='confirmation date', null=True, blank=True,
    )
    is_old_phone_confirmed = models.BooleanField(
        verbose_name='is old phone confirmed', default=False,
    )
    user_1C_code = models.CharField(
        max_length=255, null=True, blank=True,
        verbose_name='Уникальный 1С код пользователя'
    )
    is_corporate_account = models.BooleanField(
        default=False, verbose_name='Корпоративный аккаунт?'
    )
    objects = CustomUserManager()

    USERNAME_FIELD = 'phone'
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
        constraints = [
            UniqueConstraint(
                fields=['user_1C_code'], condition=~Q(user_1C_code=None),
                name='unique_user_1C_code_exp_null')
        ]

    def __str__(self):
        return f'{self.phone} {self.first_name}'


class City(models.Model):
    title = models.CharField(max_length=200, verbose_name='Город')

    class Meta:
        verbose_name = 'Город'
        verbose_name_plural = 'Города'

    def __str__(self):
        return self.title
