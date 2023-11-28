# Generated by Django 4.2.5 on 2023-11-22 16:28

import django.contrib.postgres.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Hackaton', '0002_rename_descriptionshort_hackaton_description_short'),
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