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
            name='Graduation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=150, unique=True, verbose_name='Заголовок')),
            ],
            options={
                'verbose_name': 'Уровень образования',
                'verbose_name_plural': 'Уровень образования',
            },
        ),
        migrations.CreateModel(
            name='Resume',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=150, verbose_name='Заголовок')),
                ('description', models.TextField(verbose_name='Описание')),
                ('visible', models.BooleanField(default=True, verbose_name='Видимость')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='resume', to=settings.AUTH_USER_MODEL, unique=True)),
            ],
            options={
                'verbose_name': 'Резюме',
                'verbose_name_plural': 'Резюме',
            },
        ),
        migrations.CreateModel(
            name='Work',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=150, verbose_name='Заголовок')),
                ('description', models.TextField(verbose_name='Описание')),
                ('begin', models.DateTimeField(null=True, verbose_name='Начало')),
                ('end', models.DateTimeField(null=True, verbose_name='Конец')),
                ('resume', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='work', to='Resume.resume')),
            ],
            options={
                'verbose_name': 'Работа',
                'verbose_name_plural': 'Работа',
            },
        ),
        migrations.CreateModel(
            name='Hackatons',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=150, verbose_name='Заголовок')),
                ('description', models.TextField(verbose_name='Описание')),
                ('begin', models.DateTimeField(null=True, verbose_name='Начало хакатона')),
                ('end', models.DateTimeField(null=True, verbose_name='Конец хакатона')),
                ('place', models.IntegerField(verbose_name='Место')),
                ('resume', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='hackatons', to='Resume.resume')),
            ],
            options={
                'verbose_name': 'Хакатоны',
                'verbose_name_plural': 'Хакатоны',
            },
        ),
        migrations.CreateModel(
            name='Education',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=150, verbose_name='Заголовок')),
                ('begin', models.DateTimeField(null=True, verbose_name='Начало образования')),
                ('end', models.DateTimeField(null=True, verbose_name='Окончание образования')),
                ('graduation', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='Resume.graduation', verbose_name='Уровень образования')),
                ('resume', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='educaion', to='Resume.resume')),
            ],
            options={
                'verbose_name': 'Образование',
                'verbose_name_plural': 'Образование',
            },
        ),
        migrations.CreateModel(
            name='Contact',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=150, verbose_name='Заголовок')),
                ('body', models.TextField(verbose_name='Тело контакта')),
                ('resume', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='contact', to='Resume.resume')),
            ],
            options={
                'verbose_name': 'Контакты',
                'verbose_name_plural': 'Контакты',
            },
        ),
    ]
