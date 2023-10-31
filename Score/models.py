from django.db import models
from django.contrib.auth.models import User # пока со стандартным пользователем связываемся
import datetime


'''
нужно уточнить про таблицы, что будет хранится
'''
# Create your models here.
class PointCondition(models.Model):
    user = models.ForeignKey(User, on_delete=models.PROTECT, unique=True,
                             related_name="PointConditionUserID", verbose_name='user_id') #to_field='можно свое указать'
    title = models.CharField(max_length=150, verbose_name="Заголовок")
    class Meta:
        verbose_name = "Состояние точки"   # как правильнее? не понял про что таблица
        verbose_name_plural = "Состояние точки"
    def __str__(self):
        return f'id: {self.pk}'


class HistoryPoint(models.Model):
    user = models.ForeignKey(User, on_delete=models.PROTECT, unique=True, related_name="HistoryPointUserID")
    condition = models.ForeignKey(PointCondition, on_delete=models.CASCADE, null=True,
                                  verbose_name="condition_id",  related_name="conditionID") #unique=True?

    count = models.IntegerField(verbose_name="Количество")
    created = models.DateTimeField(default=datetime.datetime.now, verbose_name="Время создания")

    class Meta:
        verbose_name = "История" # как правильнее? не понял про что таблица
        verbose_name_plural = "История"
    def __str__(self):
        return f'user_id: {self.user}, condition: {self.condition}'