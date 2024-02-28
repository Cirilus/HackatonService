from django.db import models
from django.contrib.auth import get_user_model
from users.models import User
from django.core.exceptions import ValidationError
from django.contrib.postgres.fields import ArrayField
import datetime
from django.core.validators import FileExtensionValidator




class Parser_Test(models.Model):
    title = models.CharField(verbose_name='Название хакатона', blank=True, default='Нет данных', max_length=255)
    image_url = models.URLField(max_length=500, verbose_name='Ссылка на изображение')
    creator = models.CharField(verbose_name='Организаторы хакатона', blank=True, default='Нет данных')
    grand_prize = models.TextField( blank=True, verbose_name='Призовой фонд', default='Нет данных')
    end_registration = models.CharField(verbose_name='Конец регистрации на хакатон', blank=True, default='Нет данных', max_length=255)
    about = models.TextField(verbose_name='Технологический фокус хакатона', blank=True, default='Нет данных')
    target_audience = models.TextField(blank=True, verbose_name='Для кого хакатон', default='Нет данных' )
    date_hackaton = models.CharField(verbose_name='Даты проведения хакатона', blank=True, default='Нет данных', max_length=255)
    location = models.CharField(blank=True, verbose_name='Место проведения хакатона', null=True, default='Нет данных', max_length=255)
    is_online = models.BooleanField(default=False, verbose_name='Будет ли возможность онлайн участия', blank=True)
    hackaton_link = models.URLField(max_length=255, verbose_name='Ссылка на хакатон')

    def __str__(self):
        return self.title + " by " + self.creator


class Hackaton(models.Model):
    title = models.CharField(max_length=150)
    image_url = models.FileField(upload_to='hackatons/')
    description = models.TextField()
    description_short = models.TextField()
    creator = models.CharField(max_length=150)

    start_registration = models.DateTimeField(default=datetime.datetime.now)
    end_registration = models.DateTimeField()
    start = models.DateTimeField(default=datetime.datetime.now)
    end = models.DateTimeField()

    grand_prize = models.CharField(max_length=150, blank=True)
    roles = ArrayField(models.CharField(max_length=150), default=list)
    location = models.CharField(max_length=150, blank=True)
    is_online = models.BooleanField(default=True)

    #hackaton_url = models.URLField(max_length=200, blank=True, null=True)
    #добавить линк на хакатон для перехода


    def __str__(self):
        return self.title + " " + self.creator
    
    def clean(self):
        if self.image_url.size > 3 * 1024 * 1024 * 8:
            raise ValidationError('image size is too large')


class Track(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    hackaton = models.ForeignKey(Hackaton, related_name='tracks', on_delete=models.CASCADE)


class Hackaton_User(models.Model):
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    hackaton = models.ForeignKey(Hackaton, on_delete=models.PROTECT)
    place = models.IntegerField()

    def __str__(self):
       return self.user.middle_name + ' ' + self.hackaton.title + ' ' + str(self.user.pk)
    
    class Meta:
        unique_together = ('user', 'hackaton')


class Team(models.Model):
    title = models.CharField(max_length=150)
    description = models.TextField()
    hackaton = models.ForeignKey(Hackaton, on_delete=models.PROTECT)
    owner = models.ForeignKey(Hackaton_User, on_delete=models.PROTECT)

    def clean(self):
        if self.owner.hackaton != self.hackaton:
            raise ValidationError('error')
        
    def __str__(self):
        return f'id: {self.pk}, title: {self.title}'


class User_Team(models.Model):
    user = models.ForeignKey(Hackaton_User, on_delete=models.PROTECT)
    team = models.ForeignKey(Team, on_delete=models.PROTECT)
    is_invited = models.BooleanField(default=True)

    def clean(self):
        if self.team.owner.hackaton != self.user.hackaton:
            raise ValidationError('error')
        
    def __str__(self):
        return self.user.user.middle_name + ' ' + self.team.hackaton.title + ' ' + self.team.title


class JoinRequest(models.Model):
    status_choice = [('accept', 'accept'),
                     ('pending', 'pending'),
                     ('decline', 'decline')]
    user = models.ForeignKey(Hackaton_User, on_delete=models.CASCADE)
    team = models.ForeignKey(Team, on_delete=models.CASCADE)
    status = models.CharField(max_length=15, choices=status_choice, default='pending')