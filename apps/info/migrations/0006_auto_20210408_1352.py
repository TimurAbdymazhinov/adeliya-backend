# Generated by Django 2.2.16 on 2021-04-08 07:52

import core.utils
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('info', '0005_auto_20210408_1140'),
    ]

    operations = [
        migrations.CreateModel(
            name='ContactIcon',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=70, verbose_name='Заголовок иконки')),
                ('image', models.ImageField(upload_to=core.utils.generate_filename, verbose_name='Фото иконки для контактов')),
            ],
            options={
                'verbose_name': 'Иконка для контактов',
                'verbose_name_plural': 'Иконки для контактов',
            },
        ),
        migrations.RemoveField(
            model_name='contact',
            name='icon_type',
        ),
        migrations.AddField(
            model_name='contact',
            name='icon_image',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='contacts', to='info.ContactIcon', verbose_name='Иконка'),
            preserve_default=False,
        ),
    ]
