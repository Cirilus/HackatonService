# Generated by Django 4.2.6 on 2023-10-26 10:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Resume', '0002_alter_education_graduation'),
    ]

    operations = [
        migrations.AlterField(
            model_name='education',
            name='begin',
            field=models.DateTimeField(null=True),
        ),
        migrations.AlterField(
            model_name='education',
            name='end',
            field=models.DateTimeField(null=True),
        ),
        migrations.AlterField(
            model_name='hackatons',
            name='begin',
            field=models.DateTimeField(null=True),
        ),
        migrations.AlterField(
            model_name='hackatons',
            name='end',
            field=models.DateTimeField(null=True),
        ),
        migrations.AlterField(
            model_name='work',
            name='begin',
            field=models.DateTimeField(null=True),
        ),
        migrations.AlterField(
            model_name='work',
            name='end',
            field=models.DateTimeField(null=True),
        ),
    ]