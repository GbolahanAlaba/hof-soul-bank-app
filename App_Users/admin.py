# Register your models here.
from django.contrib import admin
from . models import *

class AuthAdmin(admin.ModelAdmin):
    list_display = ['sector', 'role', 'auth_code']
    list_filter = ['sector']
    search_fields = ['sector']

class UserAdmin(admin.ModelAdmin):
    list_display = ['first_name', 'last_name', 'phone_number', 'email', 'role', 'sector']
    list_filter = ['first_name']
    search_fields = ['first_name']

class RoleAdmin(admin.ModelAdmin):
    list_display = ['role_name', 'created_by', 'id', 'timestamp']
    list_filter = ['role_name']
    search_fields = ['role_name']

class SectorAdmin(admin.ModelAdmin):
    list_display = ['sector_name', 'created_by', 'id', 'timestamp']
    list_filter = ['sector_name']
    search_fields = ['sector_name']


admin.site.register(User, UserAdmin)
admin.site.register(Roles, RoleAdmin)
admin.site.register(Sectors, SectorAdmin)
admin.site.register(AuthCode, AuthAdmin)
