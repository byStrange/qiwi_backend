# Generated by Django 4.2 on 2023-06-18 21:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0021_ad_images'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='ad',
            name='images',
        ),
        migrations.AddField(
            model_name='ad',
            name='image_size_1',
            field=models.ImageField(blank=True, null=True, upload_to='ads_images/size_1'),
        ),
        migrations.AddField(
            model_name='ad',
            name='image_size_2',
            field=models.ImageField(blank=True, null=True, upload_to='ads_images/size_2'),
        ),
    ]