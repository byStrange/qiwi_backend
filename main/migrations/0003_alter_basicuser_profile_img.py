# Generated by Django 4.2 on 2023-05-07 05:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0002_alter_basicuser_phone_number'),
    ]

    operations = [
        migrations.AlterField(
            model_name='basicuser',
            name='profile_img',
            field=models.ImageField(blank=True, null=True, upload_to='profile_pictures/'),
        ),
    ]
