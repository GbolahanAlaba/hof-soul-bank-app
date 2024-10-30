from . models import *
from django.contrib.auth import get_user_model
from rest_framework.response import Response
from rest_framework import generics
from rest_framework import viewsets, permissions
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken 
from rest_framework.authtoken.serializers import AuthTokenSerializer
from knox.auth import TokenAuthentication
from rest_framework.views import APIView
from knox.auth import AuthToken
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication 
from . serializers import *
from . utils import *
from django.db.models import Q
from rest_framework.decorators import action




class SetupViewSets(viewsets.ViewSet):
    authentication_classes=[JWTAuthentication]
    permission_classes=[IsAuthenticated]

    @handle_exceptions
    def create_auth_code(self, request):
        user = request.user

        if user.role != "Sector Leader":
            return Response({"status": "failed", "message": "Unauthorized"}, status=status.HTTP_403_FORBIDDEN)
        else:
            auth = {'hof': 'HOF'}
            auth_code = "{}{}".format(auth ['hof'], randint(100000, 999999))
            AuthCode.objects.create(auth_code=auth_code)
            return Response({"status": "success", "message": f"Authorization code created '{auth_code}'", "data": auth_code}, status=status.HTTP_201_CREATED)
    

    @handle_exceptions
    def create_team(self, request):
        user = request.user

        if not user.is_admin:
            return Response({"status": "failed", "message": "Unauthorized"}, status=status.HTTP_403_FORBIDDEN)
        elif Team.objects.filter(name=request.data.get("name")):
            return Response({"status": "failed", "message": "Team already exists"}, status=status.HTTP_409_CONFLICT)
        else:
            serializer = TeamSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save(created_by=user)
            return Response({"status": "success", "message": f"Team created successfully'", "data": serializer.data}, status=status.HTTP_201_CREATED)
        
    @handle_exceptions
    def create_sector(self, request):
        user = request.user

        if not user.is_admin:
            return Response({"status": "failed", "message": "Unauthorized"}, status=status.HTTP_403_FORBIDDEN)
        elif Sector.objects.filter(name=request.data.get("name")):
            return Response({"status": "failed", "message": "Sector already exists"}, status=status.HTTP_409_CONFLICT)
        else:
            serializer = SectorSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save(created_by=user)
            return Response({"status": "success", "message": f"Team created successfully'", "data": serializer.data}, status=status.HTTP_201_CREATED)
