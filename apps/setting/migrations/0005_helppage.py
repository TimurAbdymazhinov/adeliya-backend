# Generated by Django 2.2.16 on 2021-05-17 10:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('setting', '0004_auto_20210505_1513'),
    ]

    operations = [
        migrations.CreateModel(
            name='HelpPage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=50, verbose_name='Заголовок справки')),
                ('text', models.TextField(verbose_name='Текст справки')),
            ],
            options={
                'verbose_name': 'Справка',
                'verbose_name_plural': 'Справки',
            },
        ),
    ]
