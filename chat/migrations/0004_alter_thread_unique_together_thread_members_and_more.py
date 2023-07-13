# Generated by Django 4.2 on 2023-06-22 09:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0026_testdata'),
        ('chat', '0003_alter_chatmessage_user'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='thread',
            unique_together=set(),
        ),
        migrations.AddField(
            model_name='thread',
            name='members',
            field=models.ManyToManyField(to='main.basicuser'),
        ),
        migrations.RemoveField(
            model_name='thread',
            name='first_person',
        ),
        migrations.RemoveField(
            model_name='thread',
            name='second_person',
        ),
    ]