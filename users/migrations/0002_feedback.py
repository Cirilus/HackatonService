# Generated by Django 4.2.7 on 2023-12-05 16:59

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Feedback',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('contact_back', models.CharField(blank=True, max_length=150, verbose_name='Способ связи с пользователем')),
                ('feedback_massage', models.TextField(verbose_name='Фидбек пользователя')),
                ('create_at', models.DateTimeField(auto_now_add=True, verbose_name='Время создания фидбек-месседжа')),
                ('status', models.CharField(choices=[('New', 'New'), ('Current', 'Current'), ('Completed', 'Completed')], default='New', max_length=60, verbose_name='Статус заявки')),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='feedback', to=settings.AUTH_USER_MODEL, verbose_name='user_id')),
            ],
            options={
                'verbose_name': 'Обратная связь',
                'verbose_name_plural': 'Обратная связь',
            },
        ),
    ]
