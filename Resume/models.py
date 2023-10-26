from django.db import models
from django.contrib.auth.models import User

import datetime
# Create your models here.


class Resume(models.Model): #получить все резюме, отправить все резюме, изменить удалить
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    title = models.CharField(max_length=150)
    description = models.TextField()
    visible = models.BooleanField(default=True)

    def __str__(self):
        return f'title: {self.title}'

class Graduation(models.Model): #post, get, delete upd
    title = models.CharField(max_length=150)

    def __str__(self):
        return f'title: {self.title}'

class Education(models.Model):
    resume = models.ForeignKey(Resume, on_delete=models.CASCADE)
    graduation = models.ForeignKey(Graduation, on_delete=models.CASCADE, null=True)
    title = models.CharField(max_length=150)
    begin = models.DateTimeField(null=True) #default=datetime.datetime.now ???
    end = models.DateTimeField(null=True)

    def __str__(self):
        return f'resume_id: {self.resume_id}, graduation: {self.graduation}, -> {self.title}'


class Work(models.Model):
    resume = models.ForeignKey(Resume, on_delete=models.CASCADE)
    title = models.CharField(max_length=150)
    description = models.TextField()
    begin = models.DateTimeField(null=True) #default=datetime.datetime.now ???
    end = models.DateTimeField(null=True)

    def __str__(self):
        return f'resume_id: {self.resume_id}, -> {self.title}'



class Contact(models.Model):
    resume = models.ForeignKey(Resume, on_delete=models.CASCADE)
    title = models.CharField(max_length=150)
    body = models.TextField()

    def __str__(self):
        return f'resume_id: {self.resume_id}, -> {self.title}'


class Hackatons(models.Model):
    resume = models.ForeignKey(Resume, on_delete=models.CASCADE)
    title = models.CharField(max_length=150)
    description = models.TextField()
    begin = models.DateTimeField(null=True) #default=datetime.datetime.now ???
    end = models.DateTimeField(null=True)
    place = models.TextField()

    def __str__(self):
        return f'resume_id: {self.resume_id}, -> {self.title}'



