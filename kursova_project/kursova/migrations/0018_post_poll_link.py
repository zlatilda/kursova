# Generated by Django 2.1.7 on 2019-04-30 09:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('kursova', '0017_remove_post_poll_link'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='poll_link',
            field=models.TextField(default=''),
        ),
    ]
