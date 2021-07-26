# Generated by Django 2.2 on 2021-03-29 07:58

import apps.account.models
import core.utils
from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0011_update_proxy_permissions'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('first_name', models.CharField(blank=True, max_length=30, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('email', models.EmailField(blank=True, max_length=254, verbose_name='email address')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('phone', models.CharField(max_length=25, unique=True, verbose_name='Телефон')),
                ('avatar', models.ImageField(blank=True, null=True, upload_to=core.utils.generate_filename, verbose_name='Аватар')),
                ('birth_date', models.DateField(null=True, verbose_name='Дата рождения')),
                ('gender', models.CharField(choices=[('male', 'Мужской'), ('female', 'Женский')], default='male', max_length=10, verbose_name='Пол')),
                ('active_point', models.PositiveIntegerField(default=0, verbose_name='Активные баллы')),
                ('inactive_point', models.PositiveIntegerField(default=0, verbose_name='Неактивные баллы')),
                ('discount', models.SmallIntegerField(default=0, verbose_name='Скидка')),
                ('qr_code', models.CharField(max_length=255, null=True, verbose_name='QR-код')),
                ('qr_code_updated_at', models.DateTimeField(null=True, verbose_name='QR-код обновлен в')),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'Пользователь',
                'verbose_name_plural': 'Пользователи',
            },
            managers=[
                ('objects', apps.account.models.CustomUserManager()),
            ],
        ),
    ]
