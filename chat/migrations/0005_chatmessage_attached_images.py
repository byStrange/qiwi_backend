# Generated by Django 4.2 on 2023-06-22 12:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0026_testdata'),
        ('chat', '0004_alter_thread_unique_together_thread_members_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='chatmessage',
            name='attached_images',
            field=models.ManyToManyField(to='main.image'),
        ),
    ]
