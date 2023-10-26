from django.db import models
from django.contrib.auth.models import User, AbstractBaseUser, BaseUserManager, PermissionsMixin

import datetime
# Create your models here.

class User(AbstractBaseUser, PermissionsMixin):
    '''
    из ветки custom_user. Она не запушена
    '''
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    middle_name = models.CharField(max_length=30)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=15)
    count_point = models.IntegerField(default=0)

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name', 'middle_name', 'phone']

    # objects = UserManager()

    def __str__(self):
        return self.email
class Resume(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.PROTECT)
    title = models.CharField(max_length=150)
    description = models.TextField()
    visible = models.BooleanField(default=True)

    def __str__(self):
        return f'title: {self.title}'

class Graduation(models.Model):
    title = models.CharField(max_length=150)

    def __str__(self):
        return f'title: {self.title}'

class Education(models.Model):
    resume_id = models.ForeignKey(Resume, on_delete=models.CASCADE)
    graduation = models.ForeignKey(Graduation, on_delete=models.CASCADE)
    title = models.CharField(max_length=150)
    begin = models.DateTimeField() #default=datetime.datetime.now ???
    end = models.DateTimeField()

    def __str__(self):
        return f'resume_id: {self.resume_id}, graduation: {self.graduation}, -> {self.title}'


class Work(models.Model):
    resume_id = models.ForeignKey(Resume, on_delete=models.CASCADE)
    title = models.CharField(max_length=150)
    description = models.TextField()
    begin = models.DateTimeField() #default=datetime.datetime.now ???
    end = models.DateTimeField()

    def __str__(self):
        return f'resume_id: {self.resume_id}, -> {self.title}'



class Contact(models.Model):
    resume_id = models.ForeignKey(Resume, on_delete=models.CASCADE)
    title = models.CharField(max_length=150)
    body = models.TextField()

    def __str__(self):
        return f'resume_id: {self.resume_id}, -> {self.title}'


class Hackatons(models.Model):
    resume_id = models.ForeignKey(Resume, on_delete=models.CASCADE)
    title = models.CharField(max_length=150)
    description = models.TextField()
    begin = models.DateTimeField() #default=datetime.datetime.now ???
    end = models.DateTimeField()
    place = models.TextField()

    def __str__(self):
        return f'resume_id: {self.resume_id}, -> {self.title}'






