import datetime

from django.db import models

from solo.models import SingletonModel


class TimeStampAbstractModel(models.Model):

    created_at = models.DateTimeField(
        verbose_name='Создано', auto_now_add=True, null=True
    )
    updated_at = models.DateTimeField(
        verbose_name='Обновлено', auto_now=True, null=True
    )

    def __unicode__(self):
        pass

    def __str__(self):
        return self.__unicode__()

    class Meta:
        abstract = True


class Setting(SingletonModel):
    qr_code_expiration_date = models.DurationField(
        default=datetime.timedelta(minutes=3),
        verbose_name='Срок активности QR кода',
        help_text=' QR код будет недействителен при истечений срока активности'
    )
    is_service_active = models.BooleanField(
        default=True, verbose_name='Статус сервиса',
        help_text='Убрав галочку, вы можете отключить сервис'
    )

    def __str__(self):
        return f'Статус сайта: {self.is_service_active}'

    class Meta:
        verbose_name = 'Настройка сайта'
        verbose_name_plural = 'Настройки сайта'


class AppVersion(SingletonModel):
    android_version = models.CharField(
        max_length=15, verbose_name='Версия для android приложения',
    )
    android_force_update = models.BooleanField(
        default=False, verbose_name='Принудительное обновление(Вкл/Выкл)',
    )
    ios_build_number = models.PositiveIntegerField(
        verbose_name='Build версия для ios приложения', null=True
    )
    ios_version = models.CharField(
        max_length=15, verbose_name='Версия для ios приложения',
    )
    ios_force_update = models.BooleanField(
        default=False, verbose_name='Принудительное обновление(Вкл/Выкл)',
    )

    def __str__(self):
        return f'Android v{self.android_version}, ios v{self.ios_version}'

    class Meta:
        verbose_name = 'Версия мобильного приложения'
        verbose_name_plural = 'Версии мобильного приложения'


class HelpPage(SingletonModel):
    title = models.CharField(
        max_length=50, verbose_name="Заголовок справки",
    )
    text = models.TextField(verbose_name="Текст справки")

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Справка'
        verbose_name_plural = 'Справки'
