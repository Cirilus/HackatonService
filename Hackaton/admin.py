from django.contrib import admin
from .models import *


class HackatonAdmin(admin.ModelAdmin):
    list_display = ('pk', 'title', 'creator', 'start_registration', 'end_registration', 'start', 'end')
    search_fields = ['title', 'creator',]


admin.site.register(Hackaton, HackatonAdmin)
admin.site.register(Hackaton_User)
admin.site.register(Team)
admin.site.register(User_Team)
