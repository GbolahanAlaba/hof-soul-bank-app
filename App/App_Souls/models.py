from django.db import models
from App_Users.models import *
# Create your models here.

class Soul(models.Model):
    won_by = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True, default='')
    full_name = models.CharField(max_length=50, blank=True, null=True, default='')
    phone_number = models.CharField(max_length=50, blank=True, null=True, default='')
    address = models.CharField(max_length=50, blank=True, null=True, default='')
    status = models.CharField(max_length=50, blank=True, null=True, default='')
    sector = models.CharField(max_length=50, blank=True, null=True, default='')
    gender = models.BooleanField(default=True)
    age_range = models.CharField(max_length=50, blank=True, null=True, default='')
    description = models.TextField(max_length=50, blank=True, null=True, default='')
    timestamp = models.DateTimeField(auto_now_add = True)