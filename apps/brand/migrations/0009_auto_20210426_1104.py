# Generated by Django 2.2.16 on 2021-04-26 05:04

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('brand', '0008_auto_20210415_1834'),
    ]

    operations = [
        migrations.AlterField(
            model_name='filial',
            name='filial_1c_code',
            field=models.CharField(default=django.utils.timezone.now, max_length=255, unique=True, verbose_name='Уникальный 1C код филиала'),
            preserve_default=False,
        ),
    ]
