# Register your models here.
from django.contrib import admin
from . models import *


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ['first_name', 'last_name', 'phone', 'email', 'role', 'sector', 'auth_code']
    list_filter = ['first_name']
    search_fields = ['first_name']
