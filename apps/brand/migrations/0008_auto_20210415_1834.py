# Generated by Django 2.2.16 on 2021-04-15 12:34

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('brand', '0007_filial_unique_1c_filial_code'),
    ]

    operations = [
        migrations.RenameField(
            model_name='filial',
            old_name='unique_1c_filial_code',
            new_name='filial_1c_code',
        ),
    ]
