# Generated by Django 2.1.7 on 2019-04-30 08:31

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('kursova', '0013_auto_20190430_1125'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='comment',
            name='poll',
        ),
        migrations.RemoveField(
            model_name='comment',
            name='user',
        ),
        migrations.DeleteModel(
            name='Comment',
        ),
    ]