# Generated by Django 4.0.1 on 2022-01-28 11:33

import apps.users.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='image',
            field=models.ImageField(upload_to=apps.users.models.user_directory_path, verbose_name='Image'),
        ),
    ]
