# Generated by Django 4.2.6 on 2023-10-31 01:09

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
            name='PointCondition',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=150, verbose_name='Заголовок')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='PointConditionUserID', to=settings.AUTH_USER_MODEL, unique=True)),
            ],
            options={
                'verbose_name': 'Состояние точки',
                'verbose_name_plural': 'Состояние точки',
            },
        ),
        migrations.CreateModel(
            name='HistoryPoint',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('count', models.IntegerField(verbose_name='Количество')),
                ('created', models.DateTimeField(default=datetime.datetime.now, verbose_name='Время создания')),
                ('condition', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='conditionID', to='Score.pointcondition', verbose_name='Состояние')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='HistoryPointUserID', to=settings.AUTH_USER_MODEL, unique=True)),
            ],
            options={
                'verbose_name': 'История',
                'verbose_name_plural': 'История',
            },
        ),
    ]
