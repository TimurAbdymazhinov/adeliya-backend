# Generated by Django 2.2.16 on 2021-04-12 11:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('brand', '0006_auto_20210407_1607'),
    ]

    operations = [
        migrations.AddField(
            model_name='filial',
            name='unique_1c_filial_code',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='Уникальный 1C код филиала'),
        ),
    ]
