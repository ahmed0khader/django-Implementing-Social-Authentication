# Generated by Django 4.1.5 on 2023-01-29 15:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('images', '0002_rename_user_like_image_users_like'),
    ]

    operations = [
        migrations.AlterField(
            model_name='image',
            name='image',
            field=models.ImageField(upload_to='images/%Y/%m/%d/'),
        ),
    ]
