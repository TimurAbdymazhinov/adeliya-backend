# Generated by Django 2.2.16 on 2021-05-27 05:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0008_user_is_corporate_account'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='qr_code',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='QR-код'),
        ),
        migrations.AlterField(
            model_name='user',
            name='qr_code_updated_at',
            field=models.DateTimeField(blank=True, null=True, verbose_name='QR-код обновлен в'),
        ),
    ]
