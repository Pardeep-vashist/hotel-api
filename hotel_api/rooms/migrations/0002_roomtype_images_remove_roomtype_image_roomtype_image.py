# Generated by Django 5.2.3 on 2025-06-27 07:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rooms', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='RoomType_Images',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to='room_images/')),
            ],
        ),
        migrations.RemoveField(
            model_name='roomtype',
            name='image',
        ),
        migrations.AddField(
            model_name='roomtype',
            name='image',
            field=models.ManyToManyField(to='rooms.roomtype_images'),
        ),
    ]
