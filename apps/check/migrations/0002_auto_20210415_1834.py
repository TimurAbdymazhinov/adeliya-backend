# Generated by Django 2.2.16 on 2021-04-15 12:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('check', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='check',
            name='filial_1c_code',
            field=models.CharField(max_length=255, null=True, verbose_name='Уникальный 1C код филиала'),
        ),
        migrations.AddField(
            model_name='check',
            name='user_1c_code',
            field=models.CharField(max_length=255, null=True, verbose_name='Уникальный 1C код пользователя'),
        ),
    ]
