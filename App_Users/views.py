from django.shortcuts import render
from django.http import JsonResponse
from django.shortcuts import render

from . models import *
from django.contrib.auth import get_user_model
from rest_framework.decorators import api_view
from django.contrib.auth import login, logout, authenticate
from rest_framework.response import Response
from rest_framework import generics
from rest_framework import status
from rest_framework.authtoken.serializers import AuthTokenSerializer
from knox.auth import TokenAuthentication
from rest_framework.views import APIView
from knox.auth import AuthToken
from rest_framework.permissions import IsAuthenticated
from . serializers import *
import re

def is_valid_email(email):
      # Define the regex pattern for email validation
      pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
      return re.match(pattern, email)

# Create your views here.
class CreateAuthCode(generics.GenericAPIView):
    serializer_class = AuthCodeSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        auth_user = User.objects.get(id=self.request.user.id)

        if auth_user.role != 'Admin' and auth_user.role != 'Sector Leader':
            return Response({"error": "You don't have access to generate authentication code"}, status=status.HTTP_401_UNAUTHORIZED)
        else:
            auth = {'hof': 'HOF'}
            auth_key = "{}{}".format(auth ['hof'], randint(100000, 999999))
            serializer = self.serializer_class(data=request.data)
            serializer.is_valid(raise_exception=True)
            saveauth = serializer.save()
            saveauth.auth_code = auth_key
            saveauth.save()
            return Response({'This is your code %s'%(auth_key)}, status=status.HTTP_200_OK)
        
class Signin(generics.GenericAPIView):
    serializer_class = AuthTokenSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        
        _, token = AuthToken.objects.create(user)     

        return Response({
            'user_info':{
                'id': user.id,
                'first_name': user.first_name,
                'last_name': user.last_name,
                'email': user.email,
                'phone_number': user.phone_number,
                'team': user.email,
                'role': user.role,
                'sector': user.sector,
            
            },
        'token': token
        }, status=status.HTTP_200_OK)
    
class Signup(generics.GenericAPIView):
    serializer_class = SignupSerializer
    
    def post(self, request, *args, **kwargs):
        email = request.data['email']
        auth_code = request.data['auth_code']
        
        if not AuthCode.objects.filter(auth_code=auth_code):
            return Response({"error":"Invalid auth_code"}, status=status.HTTP_401_UNAUTHORIZED)
        elif not is_valid_email(email):
            return Response({"error":"Invalid email"}, status=status.HTTP_401_UNAUTHORIZED)
        elif User.objects.filter(email=email):
            return Response({'error':'Email exist'}, status=status.HTTP_401_UNAUTHORIZED)
        elif User.objects.filter(email=email):
            return Response({'error':'Email exist'}, status=status.HTTP_401_UNAUTHORIZED)
        else:            
            serializer = self.serializer_class(data=request.data)
            serializer.is_valid(raise_exception=True)
            the_user = serializer.save()
            _, token = AuthToken.objects.create(the_user)
        
            return Response({
                'user_info':{
                    'ID': the_user.id,
                    'First Name': the_user.first_name,
                    'Last Name': the_user.last_name,
                    'Phone Number': the_user.phone_number,
                    'Email': the_user.email,
                    "Gender": the_user.gender,
                    'Role': the_user.role,
                    'Sector': the_user.sector,
                    
                },
            'token': token
            }, status=status.HTTP_201_CREATED)

class Create_Sector(generics.GenericAPIView):
    serializer_class = SectorSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    
    def post(self, request, *args, **kwargs):
        if get_user_model().objects.get(id=self.request.user.id).role != 'Admin':
            return Response({"error":"You don't have permission to create sector"}, status=status.HTTP_401_UNAUTHORIZED)
        else:            
            serializer = self.serializer_class(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save(created_by=self.request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
class Create_Role(generics.GenericAPIView):
    serializer_class = RoleSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    
    def post(self, request, *args, **kwargs):
        if get_user_model().objects.get(id=self.request.user.id).role != 'Admin':
            return Response({"error":"You don't have permission to create role"}, status=status.HTTP_401_UNAUTHORIZED)
        else:            
            serializer = self.serializer_class(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save(created_by=self.request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

class Update_Role(generics.GenericAPIView):
    serializer_class = RoleSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, id):
        if get_user_model().objects.get(id=self.request.user.id).role != 'Admin':
            return Response({"error":"You don't have permission to view role"}, status=status.HTTP_401_UNAUTHORIZED)
        
        try:
            obj = Roles.objects.get(id=id)
        except:
            return Response({"error":"User not found"}, status=status.HTTP_404_NOT_FOUND)

        else:
            serializer = self.serializer_class(obj)
            return Response(serializer.data, status=status.HTTP_200_OK)
    
    def put(self, request, id):
        if get_user_model().objects.get(id=self.request.user.id).role != 'Admin':
            return Response({"error":"You don't have permission to view role"}, status=status.HTTP_401_UNAUTHORIZED)
        
        try:
            obj = Roles.objects.get(id=id)
        except:
            return Response({"error":"User not found"}, status=status.HTTP_404_NOT_FOUND)
        
        else:            
            serializer = self.serializer_class(obj, data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    def delete(self, request, id):
        if get_user_model().objects.get(id=self.request.user.id).role != 'Admin':
            return Response({"error":"You don't have permission to view role"}, status=status.HTTP_401_UNAUTHORIZED)
        
        try:
            obj = Roles.objects.get(id=id)
        except:
            return Response({"error":"User not found"}, status=status.HTTP_404_NOT_FOUND)

        obj.delete()
        return Response("Deleted", status=status.HTTP_204_NO_CONTENT)

class Update_Sector(generics.GenericAPIView):
    serializer_class = SectorSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, id):
        if get_user_model().objects.get(id=self.request.user.id).role != 'Admin':
            return Response({"error":"You don't have permission to view role"}, status=status.HTTP_401_UNAUTHORIZED)
        
        try:
            obj = Sectors.objects.get(id=id)
        except:
            return Response({"error":"User not found"}, status=status.HTTP_404_NOT_FOUND)

        else:
            serializer = self.serializer_class(obj)
            return Response(serializer.data, status=status.HTTP_200_OK)
    
    def put(self, request, id):
        if get_user_model().objects.get(id=self.request.user.id).role != 'Admin':
            return Response({"error":"You don't have permission to view role"}, status=status.HTTP_401_UNAUTHORIZED)
        
        try:
            obj = Sectors.objects.get(id=id)
        except:
            return Response({"error":"User not found"}, status=status.HTTP_404_NOT_FOUND)
        
        else:            
            serializer = self.serializer_class(obj, data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    def delete(self, request, id):
        if get_user_model().objects.get(id=self.request.user.id).role != 'Admin':
            return Response({"error":"You don't have permission to view role"}, status=status.HTTP_401_UNAUTHORIZED)
        
        try:
            obj = Sectors.objects.get(id=id)
        except:
            return Response({"error":"User not found"}, status=status.HTTP_404_NOT_FOUND)

        obj.delete()
        return Response("Deleted", status=status.HTTP_204_NO_CONTENT)
