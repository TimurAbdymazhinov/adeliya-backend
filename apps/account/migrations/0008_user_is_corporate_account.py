# Generated by Django 2.2.16 on 2021-04-29 05:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0007_auto_20210414_1630'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='is_corporate_account',
            field=models.BooleanField(default=False, verbose_name='Корпоративный аккаунт?'),
        ),
    ]