from django.db import models
from users.models import User

import datetime

# Create your models here.

'''поля дат пока без автозаполнения'''


class Resume(models.Model):
    user = models.ForeignKey(User, on_delete=models.PROTECT, unique=True,
                             related_name="resume")  # to_field='можно свое указать'
    title = models.CharField(max_length=150, verbose_name="Заголовок")
    description = models.TextField(verbose_name="Описание")
    visible = models.BooleanField(default=True, verbose_name="Видимость")

    class Meta:
        verbose_name = "Резюме"
        verbose_name_plural = "Резюме"

    def __str__(self):
        return f'id: {self.pk}'


class Graduation(models.Model):
    title = models.CharField(max_length=150, verbose_name="Заголовок", unique=True)

    class Meta:
        verbose_name = "Уровень образования"
        verbose_name_plural = "Уровень образования"

    def __str__(self):
        return f'title: {self.title}'


class Education(models.Model):
    resume = models.ForeignKey(Resume, on_delete=models.CASCADE, unique=False, related_name="educaion")
    graduation = models.ForeignKey(Graduation, on_delete=models.CASCADE, null=True, verbose_name="Уровень образования")
    title = models.CharField(max_length=150, verbose_name="Заголовок")
    begin = models.DateTimeField(null=True, verbose_name="Начало образования")
    end = models.DateTimeField(null=True, verbose_name="Окончание образования")

    class Meta:
        verbose_name = "Образование"
        verbose_name_plural = "Образование"

    def __str__(self):
        return f'resume_id: {self.resume_id}, graduation: {self.graduation}, -> {self.title}'


class Work(models.Model):
    resume = models.ForeignKey(Resume, on_delete=models.CASCADE, unique=False, related_name="work")
    title = models.CharField(max_length=150, verbose_name="Заголовок")
    description = models.TextField(verbose_name="Описание")
    begin = models.DateTimeField(null=True, verbose_name="Начало")
    end = models.DateTimeField(null=True, verbose_name="Конец")

    class Meta:
        verbose_name = "Работа"
        verbose_name_plural = "Работа"

    def __str__(self):
        return f'resume_id: {self.resume_id}, -> {self.title}'


class Contact(models.Model):
    resume = models.ForeignKey(Resume, on_delete=models.CASCADE, unique=False, related_name='contact')
    title = models.CharField(max_length=150, verbose_name="Заголовок")
    body = models.TextField(verbose_name="Тело контакта")

    class Meta:
        verbose_name = "Контакты"
        verbose_name_plural = "Контакты"

    def __str__(self):
        return f'resume_id: {self.resume_id}, -> {self.title}'


class Hackatons(models.Model):
    resume = models.ForeignKey(Resume, on_delete=models.CASCADE, unique=False, related_name='hackatons')
    title = models.CharField(max_length=150, verbose_name="Заголовок")
    description = models.TextField(verbose_name="Описание")
    begin = models.DateTimeField(null=True, verbose_name="Начало хакатона")
    end = models.DateTimeField(null=True, verbose_name="Конец хакатона")
    place = models.IntegerField(verbose_name="Место")

    class Meta:
        verbose_name = "Хакатоны"
        verbose_name_plural = "Хакатоны"

    def __str__(self):
        return f'resume_id: {self.resume_id}, -> {self.title}'
