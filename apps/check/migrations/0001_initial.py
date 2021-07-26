# Generated by Django 2.2.16 on 2021-04-12 11:38

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('brand', '0007_filial_unique_1c_filial_code'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Check',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('unique_1c_check_code', models.CharField(max_length=255, unique=True, verbose_name='Уникальный 1C код чека')),
                ('money_paid', models.DecimalField(decimal_places=2, max_digits=8, verbose_name='Оплачено деньгами')),
                ('bonus_paid', models.DecimalField(decimal_places=2, max_digits=8, verbose_name='Оплачено бонусами')),
                ('total_paid', models.DecimalField(decimal_places=2, max_digits=8, verbose_name='Сумма оплаты')),
                ('accrued_point', models.PositiveIntegerField(blank=True, null=True, verbose_name='Начислено бонусов')),
                ('accrued_point_date', models.DateTimeField(blank=True, null=True, verbose_name='Дата начисления')),
                ('withdrawn_point', models.PositiveIntegerField(blank=True, null=True, verbose_name='Снято бонусов (Возврат)')),
                ('withdrawn_point_date', models.DateTimeField(blank=True, null=True, verbose_name='Дата возврата')),
                ('is_active', models.BooleanField(default=True, verbose_name='Активность чека')),
                ('filial', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='users', to='brand.Filial', verbose_name='Филиал')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='users', to=settings.AUTH_USER_MODEL, verbose_name='Пользователь')),
            ],
            options={
                'verbose_name': 'Чек',
                'verbose_name_plural': 'Чеки',
            },
        ),
    ]