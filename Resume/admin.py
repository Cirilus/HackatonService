from django.contrib import admin
from .models import Resume, Graduation, Education, Work, Contact, Hackatons


class ResumeAdmin(admin.ModelAdmin):
    list_display = ('user_id', 'title', 'visible')
    search_fields = ['title', 'user_id__username']


class GraduationAdmin(admin.ModelAdmin):
    list_display = ('title',)


class EducationAdmin(admin.ModelAdmin):
    list_display = ('resume_id', 'graduation', 'title', 'begin', 'end')


class WorkAdmin(admin.ModelAdmin):
    list_display = ('resume_id', 'title', 'begin', 'end')


class ContactAdmin(admin.ModelAdmin):
    list_display = ('resume_id', 'title')


class HackatonsAdmin(admin.ModelAdmin):
    list_display = ('resume_id', 'title', 'begin', 'end', 'place')


admin.site.register(Resume, ResumeAdmin)
admin.site.register(Graduation, GraduationAdmin)
admin.site.register(Education, EducationAdmin)
admin.site.register(Work, WorkAdmin)
admin.site.register(Contact, ContactAdmin)
admin.site.register(Hackatons, HackatonsAdmin)
