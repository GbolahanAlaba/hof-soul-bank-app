from django.contrib.auth.models import User
from . models import *
from rest_framework.response import Response
from django.contrib.auth import get_user_model
from rest_framework import serializers, validators
from django.contrib.auth import authenticate
from django.utils.translation import gettext_lazy as _
from random import randint
from rest_framework import status


class ErrorSerializer(serializers.Serializer):
    error = serializers.CharField()

class SoulSerializer(serializers.ModelSerializer):
    won_by = serializers.CharField(read_only=True)
    class Meta:
        model = Soul
        fields = ['full_name', 'phone_number', 'address', 'gender', 'age_range', 'status', 'sector', 'description', 'won_by']