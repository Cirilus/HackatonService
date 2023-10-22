# Generated by Django 4.2.5 on 2023-10-06 17:06

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Hackaton',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=150)),
                ('description', models.TextField()),
                ('creator', models.CharField(max_length=150)),
                ('start_registration', models.DateTimeField(default=datetime.datetime.now)),
                ('end_registration', models.DateTimeField()),
                ('start', models.DateTimeField(default=datetime.datetime.now)),
                ('end', models.DateTimeField()),
            ],
        ),
        migrations.CreateModel(
            name='Hackaton_User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('place', models.IntegerField()),
                ('hackaton', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Hackaton.hackaton')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Team',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=150)),
                ('description', models.TextField()),
                ('hackaton', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Hackaton.hackaton')),
            ],
        ),
        migrations.CreateModel(
            name='User_Team',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('team', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Hackaton.team')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Hackaton.hackaton_user')),
            ],
        ),
    ]
