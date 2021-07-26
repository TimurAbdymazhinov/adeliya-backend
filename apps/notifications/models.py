import ast

from django.contrib.postgres.fields import JSONField
from django.db import models
from fcm_django.models import FCMDevice

from apps.account.models import User
from core.constants import (
    ACCRUED, WITHDRAW, ACCRUED_AND_WITHDRAW,
    NEWS, PROMOTION
)
from core.constants import NOTIFICATION_TYPE
from apps.setting.models import TimeStampAbstractModel


class Notification(TimeStampAbstractModel):
    NOTIFICATION_TITLE = 'Уведомление'
    NOTIFICATION_MESSAGE = {
        ACCRUED: 'Вам начислено {accrued_point} баллов',
        WITHDRAW: 'Вы использовали {withdrawn_point} баллов',
        ACCRUED_AND_WITHDRAW: 'Вы использовали {withdrawn_point} и Вам начисленно {accrued_point} баллов',
        PROMOTION: '{title}',
        NEWS: '{title}',
    }

    user = models.ForeignKey(
        User, related_name='notifications',
        on_delete=models.CASCADE, verbose_name='Пользователь'
    )
    notice_type = models.CharField(
        choices=NOTIFICATION_TYPE, max_length=25,
        verbose_name='Тип',
    )
    is_on_credit = models.BooleanField(
        default=False, verbose_name='В долг?',
    )
    linked_article = models.ForeignKey(
        'info.PromotionAndNews', null=True, blank=True,
        related_name='notice', on_delete=models.CASCADE,
        verbose_name='Новость или Акция'
    )
    linked_check = models.ForeignKey(
        'check.Check', null=True, blank=True,
        related_name='notice', on_delete=models.CASCADE,
        verbose_name='Чек'
    )
    body = JSONField(null=True, blank=True, verbose_name='Тело')
    is_viewed = models.BooleanField(verbose_name='Просмотрено?', default=False)
    is_active = models.BooleanField(verbose_name='Активен?', default=True)

    def __str__(self):
        return f'ID: {self.id}'

    @property
    def get_message(self):
        return self.NOTIFICATION_MESSAGE[self.notice_type].format(
            **ast.literal_eval(self.body)
        )

    class Meta:
        verbose_name = 'Уведомление'
        verbose_name_plural = 'Уведомления'
        ordering = ['-created_at']
