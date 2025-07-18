# Generated by Django 5.2.3 on 2025-06-26 07:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hotels', '0004_remove_hotel_images_delete_hotel_image'),
    ]

    operations = [
        migrations.CreateModel(
            name='Hotel_Image',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to='media/Hotel Images')),
            ],
        ),
        migrations.AddField(
            model_name='hotel',
            name='images',
            field=models.ManyToManyField(to='hotels.hotel_image'),
        ),
    ]
