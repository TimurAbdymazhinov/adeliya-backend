from django.db import models
from django.forms import ValidationError

from ckeditor_uploader.fields import RichTextUploadingField
from django_2gis_maps import fields as map_fields

from core.utils import generate_filename
from core.constants import WORK_DAYS


class Brand(models.Model):
    position = models.PositiveIntegerField(
        default=0, blank=False, null=False,
        verbose_name='№',
    )
    title = models.CharField(max_length=255, verbose_name='Название')
    logo = models.ImageField(upload_to=generate_filename, verbose_name='Лого')
    description = RichTextUploadingField(
        null=True, blank=True, verbose_name='Описание'
    )
    address = models.CharField(
        max_length=100, blank=True, null=True, verbose_name='Адрес'
    )
    link = models.URLField(null=True, blank=True, verbose_name='Ссылка')

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['position']
        verbose_name = 'Бренд'
        verbose_name_plural = 'Бренды'


class BrandImage(models.Model):
    brand = models.ForeignKey(
        to='Brand', on_delete=models.CASCADE, related_name='images',
        verbose_name='Бренд'
    )
    image = models.ImageField(
        upload_to=generate_filename, verbose_name='Изображение',
    )

    def __str__(self):
        return f'Image of {self.brand.title} brand'

    class Meta:
        verbose_name = 'Изображение бренда'
        verbose_name_plural = 'Изображения бренда'


class Filial(models.Model):
    position = models.PositiveIntegerField(
        default=0, blank=False, null=False,
        verbose_name='№',
    )
    title = models.CharField(max_length=255, verbose_name='Название')
    address = map_fields.AddressField(max_length=200, verbose_name='Адрес')
    geolocation = map_fields.GeoLocationField(verbose_name='Геолокация')
    filial_1c_code = models.CharField(
        max_length=255, unique=True,
        verbose_name='Уникальный 1C код филиала'
    )

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['position']
        verbose_name = 'Филиал'
        verbose_name_plural = 'Филиалы'


class FilialImage(models.Model):
    filial = models.ForeignKey(
        to='Filial', on_delete=models.CASCADE, related_name='images',
        verbose_name='Филиал'
    )
    image = models.ImageField(
        upload_to=generate_filename, verbose_name='Изображение'
    )
    is_main = models.BooleanField(default=False, verbose_name='Основная?')

    def __str__(self):
        return f'Image of {self.filial.title} filial'

    class Meta:
        verbose_name = 'Изображение филиала'
        verbose_name_plural = 'Изображения филиала'


class FilialPhone(models.Model):
    filial = models.ForeignKey(
        to='Filial', on_delete=models.CASCADE, related_name='phone_numbers',
        verbose_name='Филиал'
    )
    phone = models.CharField(max_length=255, verbose_name='Номер телефона')
    is_phone = models.BooleanField(
        default=True, verbose_name='Номер телефона?'
    )
    is_whatsapp = models.BooleanField(
        default=True, verbose_name='Номер Whatsapp?'
    )

    def __str__(self):
        return f'Phone of {self.filial.title} filial'

    class Meta:
        verbose_name = 'Номер филиала'
        verbose_name_plural = 'Номера филиала'


class WorkTime(models.Model):
    day = models.SmallIntegerField(
        choices=WORK_DAYS, verbose_name='День недели'
    )
    start_work = models.TimeField(
        verbose_name='Начало рабочего времени', null=True, blank=True
    )
    end_work = models.TimeField(
        verbose_name='Конец рабочего времени', null=True, blank=True
    )
    filial = models.ForeignKey(
        to=Filial, on_delete=models.CASCADE, related_name='works_time',
        verbose_name='Филиал'
    )

    class Meta:
        ordering = ['day']
        unique_together = ['day', 'filial']
        verbose_name = 'Рабочий день'
        verbose_name_plural = 'Рабочие дни'

    def __str__(self):
        return f'{str(self.filial)}, {self.day}'

    def clean(self):
        text = ('Нельзя заполнить только время '
                'конца или начала, рабочего времени')
        if (
                self.start_work is None
                and self.end_work is not None
        ):
            raise ValidationError(text)
        elif (
                self.start_work is not None
                and self.end_work is None
        ):
            raise ValidationError(text)
