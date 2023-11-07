from django.db import models
from django.contrib.auth.models import User  # пока со стандартным пользователем связываемся
import datetime

'''    #нужно ли добавить проверку при добавлении записи,
        что user к которому привязан указываемый condition совпадает с юзером этого condition
'''

'''
проблема с полями со временем (см. Resume.models)
'''


# Create your models here.
class PointCondition(models.Model):  # таблица отвечает за то, при каком условии начислены очки
    user = models.ForeignKey(User, on_delete=models.PROTECT, unique=False,
                             related_name="PointConditionUserID", verbose_name='user_id',
                             null=True)  # to_field='можно свое указать'
    title = models.CharField(max_length=150, verbose_name="Условие для изменения количества очков Score")

    class Meta:
        verbose_name = "Условие начисления очков Score"
        verbose_name_plural = "Условие начисления очков Score"

    def __str__(self):
        return f'id: {self.pk}'


class HistoryPoint(models.Model):
    user = models.ForeignKey(User, on_delete=models.PROTECT, unique=False, related_name="HistoryPointUserID")
    condition = models.ForeignKey(PointCondition, on_delete=models.CASCADE, null=False,
                                  verbose_name="condition_id", related_name="conditionID", unique=True)

    count = models.IntegerField(verbose_name="Количество очков")
    created = models.DateTimeField(default=datetime.datetime.now, verbose_name="Время создания записи", null=True)

    class Meta:
        verbose_name = "Запись об изменении очков у пользователя"
        verbose_name_plural = "Запись об изменении очков у пользователя"

    def __str__(self):
        return f'user_id: {self.user}, condition: {self.condition}'
