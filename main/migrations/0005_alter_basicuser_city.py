# Generated by Django 4.2 on 2023-05-07 06:52

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0004_alter_city_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='basicuser',
            name='city',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.city'),
        ),
    ]
