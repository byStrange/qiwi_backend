# Generated by Django 4.2 on 2023-05-23 11:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0009_alter_post_city_alter_post_post_type_alter_post_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='category',
            name='icon',
            field=models.FileField(blank=True, null=True, upload_to='media/svg_icon/'),
        ),
    ]
