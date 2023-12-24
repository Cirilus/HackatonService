from django.contrib import admin
from .models import Hackaton, Hackaton_User, Team, User_Team, JoinRequest, Track


class HackatonAdmin(admin.ModelAdmin):
    list_display = ('pk', 'title', 'creator', 'start_registration', 'end_registration', 'start', 'end')
    search_fields = ['title', 'creator',]


class HackatonUserAdmin(admin.ModelAdmin):
    list_display = ('pk', 'user')


class UserTeamAdmin(admin.ModelAdmin):
    list_display = ('pk', 'user', 'team', 'is_invited')


admin.site.register(Hackaton, HackatonAdmin)
admin.site.register(Hackaton_User, HackatonUserAdmin)
admin.site.register(Team)
admin.site.register(User_Team, UserTeamAdmin)
admin.site.register(JoinRequest)
admin.site.register(Track)
