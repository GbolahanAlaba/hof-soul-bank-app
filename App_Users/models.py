from django.db import models
from App_Auth.models import *
import uuid
from django.utils import timezone


class Team(models.Model):
    team_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=50, blank=True, null=True, default='')
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True, related_name="teams")
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.name
    
class Sector(models.Model):
    sector_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=50, blank=True, null=True, default='')
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True, related_name="sectors")
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.name
    
class Role(models.Model):
    role_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True, related_name='user_role')
    admin = models.BooleanField(default=False)
    sector_lead = models.BooleanField(default=False)
    member = models.BooleanField(default=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True, related_name="roles")
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.name

class AuthCode(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    auth_code = models.CharField(max_length=50, blank=True, null=True, default='')
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.auth_code
