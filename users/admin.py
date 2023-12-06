from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Feedback

class CustomUserAdmin(admin.ModelAdmin):
    model = User
    list_display = ('pk', 'email', 'first_name', 'last_name', 'phone', 'count_point', 'is_staff')
    list_filter = ('is_staff', 'is_superuser', 'is_active')

    search_fields = ('email', 'first_name', 'last_name',)

admin.site.register(User, CustomUserAdmin)



class FeedbackAdmin(admin.ModelAdmin):
    model = Feedback
    list_display = ('user', 'contact_back', 'create_at', 'status')
    list_filter = ('user', 'contact_back', 'create_at', 'status')

    search_fields = ('user', 'contact_back', 'create_at', 'status')

admin.site.register(Feedback, FeedbackAdmin)



