# Generated by Django 4.2 on 2023-06-21 14:01

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0026_testdata'),
        ('chat', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='thread',
            name='first_person',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='thread_first_person', to='main.basicuser'),
        ),
        migrations.AlterField(
            model_name='thread',
            name='second_person',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='thread_second_person', to='main.basicuser'),
        ),
    ]