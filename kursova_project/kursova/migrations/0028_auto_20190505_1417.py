# Generated by Django 2.1.7 on 2019-05-05 11:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('kursova', '0027_images'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='images',
            name='post',
        ),
        migrations.AddField(
            model_name='images',
            name='slug',
            field=models.SlugField(default='', max_length=250, unique=True),
        ),
    ]
