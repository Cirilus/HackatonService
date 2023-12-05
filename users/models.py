from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.contrib.auth.hashers import make_password
from django.db import models
import datetime
from django.db.models.signals import post_save
from django.dispatch import receiver

class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('error email')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    first_name = models.CharField(max_length=30, blank=True)
    last_name = models.CharField(max_length=30, blank=True)
    middle_name = models.CharField(max_length=30, blank=True)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=15, blank=True)
    count_point = models.IntegerField(default=0)

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'

    objects = UserManager()

    def __str__(self):
        return self.email



class Feedback(models.Model):
    class FeedbackChoices(models.TextChoices):
        NEW = 'New', 'New'
        CURRENT = 'Current', 'Current'
        COMPLETED = 'Completed', 'Completed'

    user = models.ForeignKey(User, on_delete=models.CASCADE, unique=False,
                             related_name="feedback", verbose_name='user_id',
                             null=True)
    contact_back = models.CharField(max_length=150, verbose_name="Способ связи с пользователем", blank=True)
    feedback_massage = models.TextField(verbose_name="Фидбек пользователя")
    create_at = models.DateTimeField(auto_now_add=True, verbose_name='Время создания фидбек-месседжа')
    status = models.CharField(max_length=60, choices=FeedbackChoices.choices, default=FeedbackChoices.NEW,
                              verbose_name='Статус заявки')

    class Meta:
        verbose_name = "Обратная связь"
        verbose_name_plural = "Обратная связь"


    def __str__(self):
        return f'own_id: {self.pk}, user_id:{self.user}'

