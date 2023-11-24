from django.db import models
from django.contrib.auth import get_user_model
from users.models import User
from django.core.exceptions import ValidationError
from django.contrib.postgres.fields import ArrayField
import datetime
from django.core.validators import FileExtensionValidator

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

    tracks = ArrayField(models.CharField(max_length=150), default=list)
    grand_prize = models.CharField(max_length=150, blank=True)
    roles = ArrayField(models.CharField(max_length=150), default=list)
    location = models.CharField(max_length=150, blank=True)
    is_online = models.BooleanField(default=True)

    def __str__(self):
        return self.title + " " + self.creator
    
    def clean(self):
        if self.image_url.size > 3 * 1024 * 1024 * 8:
            raise ValidationError('image size is too large')
    

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
        return self.title + ' ' + self.hackaton.title


class User_Team(models.Model):
    user = models.ForeignKey(Hackaton_User, on_delete=models.PROTECT)
    team = models.ForeignKey(Team, on_delete=models.PROTECT)
    is_invited = models.BooleanField(default=True)

    def clean(self):
        if self.team.owner.hackaton != self.user.hackaton:
            raise ValidationError('error')
        
    def __str__(self):
        return self.user.user.middle_name + ' ' + self.team.hackaton.title + ' ' + self.team.title