from django.contrib import admin
from .models import HistoryPoint, PointCondition


# Register your models here.
class PointConditionAdmin(admin.ModelAdmin):
    list_display = ('id', 'user_id', 'title',)
    search_fields = ('id', 'user_id', 'title',)


class HistoryPointAdmin(admin.ModelAdmin):
    list_display = ('id', 'user_id', 'condition', 'count', 'created')
    search_fields = ('id', 'user_id', 'condition', 'count', 'created')


admin.site.register(PointCondition, PointConditionAdmin)
admin.site.register(HistoryPoint, HistoryPointAdmin)
