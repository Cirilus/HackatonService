from django.contrib import admin
from .models import *


class HackatonAdmin(admin.ModelAdmin):
    list_display = ('pk', 'title', 'creator', 'start_registration', 'end_registration', 'start', 'end')
    search_fields = ['title', 'creator',]


class HackatonUserAdmin(admin.ModelAdmin):
    list_display = ('pk', 'user')


class InviteTeamAdmin(admin.ModelAdmin):
    list_display = ('pk', 'team', 'user')


admin.site.register(Hackaton, HackatonAdmin)
admin.site.register(Hackaton_User, HackatonUserAdmin)
admin.site.register(Team_Invite, InviteTeamAdmin)
admin.site.register(Team)
admin.site.register(User_Team)
