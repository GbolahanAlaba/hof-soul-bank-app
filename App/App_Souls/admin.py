# Register your models here.
from django.contrib import admin
from . models import *

class SoulAdmin(admin.ModelAdmin):
    list_display = ['full_name', 'phone_number', 'address', 'status', 'gender', 'age_range', 'sector', 'id', 'won_by', 'timestamp']
    list_filter = ['full_name']
    search_fields = ['full_name']


admin.site.register(Soul, SoulAdmin)