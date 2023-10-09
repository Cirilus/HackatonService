from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
import datetime

class Hackaton(models.Model):
    title = models.CharField(max_length=150)
    description = models.TextField()
    creator = models.CharField(max_length=150)
    start_registration = models.DateTimeField(default=datetime.datetime.now)
    end_registration = models.DateTimeField()
    start = models.DateTimeField(default=datetime.datetime.now)
    end = models.DateTimeField()

    def __str__(self) -> str:
        return self.title
    

class Hackaton_User(models.Model):
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    hackaton = models.ForeignKey(Hackaton, on_delete=models.PROTECT)
    place = models.IntegerField()

    def __str__(self) -> str:
        return self.user.username + ' ' + self.hackaton.title


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

    def __str__(self) -> str:
        return self.user.user.username + ' ' + self.team.hackaton.title + ' ' + self.team.title


class Team_Invite(models.Model):
    team = models.ForeignKey(Team, on_delete=models.PROTECT)
    user = models.ForeignKey(Hackaton_User, on_delete=models.PROTECT)