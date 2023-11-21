# Generated by Django 4.2.5 on 2023-11-21 20:10

import django.contrib.postgres.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Hackaton', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='hackaton',
            name='roles',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.CharField(max_length=150), default=list, size=None),
        ),
        migrations.AddField(
            model_name='hackaton',
            name='tracks',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.CharField(max_length=150), default=list, size=None),
        ),
    ]