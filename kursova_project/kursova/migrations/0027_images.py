# Generated by Django 2.1.7 on 2019-05-05 10:34

from django.db import migrations, models
import django.db.models.deletion
import kursova.models


class Migration(migrations.Migration):

    dependencies = [
        ('kursova', '0026_auto_20190505_1311'),
    ]

    operations = [
        migrations.CreateModel(
            name='Images',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to=kursova.models.get_image_filename, verbose_name='Image')),
                ('post', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='kursova.Post')),
            ],
        ),
    ]
