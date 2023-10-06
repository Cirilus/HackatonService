from django.db import models
from django.contrib.auth.models import User
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
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    hackaton = models.ForeignKey(Hackaton, on_delete=models.CASCADE)
    place = models.IntegerField()

    def __str__(self) -> str:
        return self.user.username


class Team(models.Model):
    title = models.CharField(max_length=150)
    description = models.TextField()
    hackaton = models.ForeignKey(Hackaton, on_delete=models.CASCADE)

    def __str__(self):
        return self.title


class User_Team(models.Model):
    user = models.ForeignKey(Hackaton_User, on_delete=models.CASCADE)
    team = models.ForeignKey(Team, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return self.user.user.username

