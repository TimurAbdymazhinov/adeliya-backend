from django.db import models

from apps.account.models import User
from apps.brand.models import Filial
from core.constants import CHECK_TYPE


class Check(models.Model):
    """
        Model to save all checks from 1C
    """
    unique_1c_check_code = models.CharField(
        max_length=255, unique=True, verbose_name='Уникальный 1C код чека'
    )
    money_paid = models.DecimalField(
        null=True, blank=True,
        max_digits=8, decimal_places=2, verbose_name='Оплачено деньгами'
    )
    bonus_paid = models.DecimalField(
        null=True, blank=True,
        max_digits=8, decimal_places=2, verbose_name='Оплачено бонусами'
    )
    total_paid = models.DecimalField(
        null=True, blank=True,
        max_digits=8, decimal_places=2, verbose_name='Сумма оплаты'
    )
    accrued_point = models.DecimalField(
        null=True, blank=True,
        max_digits=8, decimal_places=2, verbose_name='Начислено бонусов'
    )
    accrued_point_date = models.DateTimeField(
        null=True, blank=True, verbose_name='Дата начисления'
    )
    withdrawn_point = models.DecimalField(
        null=True, blank=True,
        max_digits=8, decimal_places=2, verbose_name='Снято бонусов (Возврат)'
    )
    withdrawn_point_date = models.DateTimeField(
        null=True, blank=True, verbose_name='Дата возврата'
    )
    is_active = models.BooleanField(
        default=True, verbose_name='Активность чека'
    )
    user = models.ForeignKey(
        to=User, on_delete=models.CASCADE, related_name='checks',
        verbose_name='Пользователь'
    )
    filial = models.ForeignKey(
        to=Filial, null=True, on_delete=models.SET_NULL, related_name='checks',
        verbose_name='Филиал'
    )
    user_1c_code = models.CharField(
        max_length=255, null=True, verbose_name='Уникальный 1C код пользователя'
    )
    filial_1c_code = models.CharField(
        max_length=255, null=True, verbose_name='Уникальный 1C код филиала'
    )
    status = models.CharField(
        choices=CHECK_TYPE, max_length=25, verbose_name='Статус чека',
    )
    due_date = models.DateTimeField(
        null=True, blank=True, verbose_name='Дата оплаты долга'
    )
    is_on_credit = models.BooleanField(default=False, verbose_name='В долг')
    balance_owed = models.DecimalField(
        null=True, blank=True,
        max_digits=8, decimal_places=2, verbose_name='Остаток долга'
    )

    def __str__(self):
        return f'Чек №{self.unique_1c_check_code}'

    class Meta:
        verbose_name = 'Чек'
        verbose_name_plural = 'Чеки'
