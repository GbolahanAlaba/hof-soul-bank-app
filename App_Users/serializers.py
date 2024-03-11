from django.contrib.auth.models import User
from . models import *
from rest_framework.response import Response
from django.contrib.auth import get_user_model
from rest_framework import serializers, validators
from django.contrib.auth import authenticate
from django.utils.translation import gettext_lazy as _
from random import randint
from rest_framework import status

class AuthCodeSerializer(serializers.ModelSerializer):
    class Meta:
        model = AuthCode
        fields = ('sector', 'role')
    
    def create(self, validated_data):
        sector = validated_data.get('sector')
        role = validated_data.get('role')

        get_auth = AuthCode.objects.create(sector=sector, role=role)
        return get_auth

class SignupSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email', 'phone_number', 'gender', 'team', 'auth_code', 'password')
    
    def create(self, validated_data):
        first_name = validated_data.get('first_name')
        last_name = validated_data.get('last_name')
        email = validated_data.get('email')
        phone_number = validated_data.get('phone_number')
        gender = validated_data.get('gender')
        team = validated_data.get('team')
        auth_code = validated_data.get('auth_code')
        password = validated_data.get('password')

        get_sector = AuthCode.objects.get(auth_code=auth_code).sector
        get_role = AuthCode.objects.get(auth_code=auth_code).role
        
        user = get_user_model().objects.create(first_name=first_name, last_name=last_name, email=email, phone_number=phone_number, username=email, 
                                               gender=gender, team=team, sector=get_sector, role=get_role, auth_code=auth_code)
        user.set_password(password)
        user.save()

        return user

    
class AuthTokenSerializer(serializers.Serializer):
    phone_number = serializers.CharField(
        label=_("Phone_Number"),
        write_only=True
    )
    password = serializers.CharField(
        label=_("Password"),
        style={'input_type': 'password'},
        trim_whitespace=False,
        write_only=True
    )
    token = serializers.CharField(
        label=_("Token"),
        read_only=True
    )

    def validate(self, attrs):
        phone_number = attrs.get('phone_number')
        password = attrs.get('password')
    
        if phone_number and password:
            user = authenticate(request=self.context.get('request'),
                                phone_number=phone_number, password=password)

            # The authenticate call simply returns None for is_active=False
            # users. (Assuming the default ModelBackend authentication
            # backend.)
            if not user:
                # msg = _('Unable to log in with provided credentials.')
                msg =  ({"error": "Incorrect login details"})
                raise serializers.ValidationError(msg)
        else:
            msg = _('Must include "phone_number" and "password".')
            raise serializers.ValidationError(msg)

        attrs['user'] = user
        return attrs

class RoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Roles
        fields = ['role_name']

class SectorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sectors
        fields = ['sector_name']
