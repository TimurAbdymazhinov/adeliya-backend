from datetime import datetime

from django.db import models

from solo.models import SingletonModel
from ckeditor_uploader.fields import RichTextUploadingField

from core.constants import INFORMATION_TYPE, NEWS
from core.utils import generate_filename


class Banner(SingletonModel):
    title = models.CharField(
        max_length=25,
        verbose_name='Заголовок баннера',
    )
    image = models.ImageField(
        upload_to=generate_filename,
        verbose_name='Фото баннера',
    )
    description = RichTextUploadingField(
        verbose_name='Описание баннера',
    )

    class Meta:
        verbose_name_plural = 'Баннера'
        verbose_name = 'Баннер'

    def __str__(self):
        return f'{self.title}'


class ProgramCondition(SingletonModel):
    title = models.CharField(
        max_length=50,
        verbose_name='Заголовок программы лояльности',
    )
    description = RichTextUploadingField(
        verbose_name='Текст программы лояльности',
    )

    class Meta:
        verbose_name_plural = 'Программы лояльности'
        verbose_name = 'Программа лояльности'

    def __str__(self):
        return f'{self.title}'


class ContactIcon(models.Model):
    title = models.CharField(max_length=70, verbose_name='Заголовок иконки')
    image = models.ImageField(
        upload_to=generate_filename,
        verbose_name='Фото иконки для контактов',
    )

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Иконка для контактов'
        verbose_name_plural = 'Иконки для контактов'


class Contact(models.Model):
    icon_image = models.ForeignKey(
        'ContactIcon',
        on_delete=models.CASCADE,
        related_name='contacts',
        verbose_name='Иконка',
    )
    title = models.CharField(
        max_length=100,
        verbose_name='Заголовок ссылки',
    )
    link = models.CharField(
        max_length=150,
        verbose_name='Ссылка',
    )

    class Meta:
        verbose_name_plural = 'Контакты'
        verbose_name = 'Контакт'

    def __str__(self):
        return f'{self.title} {str(self.icon_image)}'


class PromotionAndNews(models.Model):
    created_at = models.DateTimeField(
        default=datetime.now, verbose_name="Дата публикации",
    )
    information_type = models.CharField(
        max_length=15,
        choices=INFORMATION_TYPE,
        default=NEWS,
        verbose_name='Тип записи',
    )
    title = models.CharField(
        max_length=100,
        verbose_name='Заголовок',
    )
    description = RichTextUploadingField(
        verbose_name='Текст статьи',
    )
    is_active = models.BooleanField(
        default=True,
        verbose_name='Активный(Вкл/Выкл)',
    )

    class Meta:
        verbose_name_plural = 'Акции и новости'
        verbose_name = 'Акция и новость'
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.title} {self.information_type}'


class PromotionAndNewsImage(models.Model):
    image = models.ImageField(
        upload_to=generate_filename,
        verbose_name='Фото новости или акции',
    )
    is_main = models.BooleanField(
        default=False,
        verbose_name='Превью(Вкл/Выкл)',
    )
    information = models.ForeignKey(
        'PromotionAndNews',
        on_delete=models.CASCADE,
        related_name="images"
    )

    class Meta:
        verbose_name_plural = 'Фотографии для акций/новости'
        verbose_name = 'Фотография для акции/новости'
        ordering = ['-is_main']
