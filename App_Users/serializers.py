from django.contrib.auth.models import User
from . models import *
from rest_framework.response import Response
from django.utils.translation import gettext_lazy as _
from random import randint
from rest_framework import status
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from rest_framework import serializers, validators


class TeamSerializer(serializers.ModelSerializer):
    created_by = serializers.SerializerMethodField()
  
    class Meta:
        model = Team
        fields = ['name', 'created_by', 'created_at', 'updated_at']

    def get_created_by(self, obj):
        return f"{obj.created_by.first_name} {obj.created_by.last_name}"
    
class SectorSerializer(serializers.ModelSerializer):
    created_by = serializers.SerializerMethodField()
  
    class Meta:
        model = Sector
        fields = ['name', 'created_by', 'created_at', 'updated_at']
    
    def get_created_by(self, obj):
        return f"{obj.created_by.first_name} {obj.created_by.last_name}"

