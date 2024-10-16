# Register your models here.
from django.contrib import admin
from . models import *


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ['first_name', 'last_name', 'phone', 'email', 'role', 'sector']
    list_filter = ['first_name']
    search_fields = ['first_name']


@admin.register(Team)
class TeamAdmin(admin.ModelAdmin):
    list_display = ['name', 'created_by', 'created_at', 'updated_at']
    list_filter = ['name']
    search_fields = ['name']


@admin.register(Sector)
class SectorAdmin(admin.ModelAdmin):
    list_display = ['name', 'created_by', 'created_at', 'updated_at']
    list_filter = ['name']
    search_fields = ['name']

@admin.register(AuthCode)
class AuthCodeAdmin(admin.ModelAdmin):
    list_display = ['auth_code', 'created_at', 'updated_at']
    list_filter = ['auth_code']
    search_fields = ['auth_code']





# admin.site.register(User, UserAdmin)
# admin.site.register(Roles, RoleAdmin)
# admin.site.register(Sectors, SectorAdmin)
# admin.site.register(AuthCode, AuthAdmin)
