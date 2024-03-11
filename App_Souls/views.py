from django.shortcuts import render
from django.http import JsonResponse
from django.shortcuts import render

from . models import *
from rest_framework.response import Response
from rest_framework import generics
from rest_framework import status
from rest_framework.authtoken.serializers import AuthTokenSerializer
from knox.auth import TokenAuthentication
from rest_framework.views import APIView
from knox.auth import AuthToken
from rest_framework.permissions import IsAuthenticated
from . serializers import *


# Create your views here.

class Create_Soul(generics.GenericAPIView):
    serializer_class = SoulSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    
    def post(self, request, *args, **kwargs):
            
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(won_by=self.request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

class Get_User_Souls(generics.GenericAPIView):
    serializer_class = SoulSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        obj = Soul.objects.filter(won_by=self.request.user)
        if not obj:
            return Response({"error":"No soul record found"}, status=status.HTTP_200_OK)

        else:
            serializer = self.serializer_class(obj, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)

class Update_User_Soul(generics.GenericAPIView):
    serializer_class = SoulSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    
    def query_set(self, request, id):
        obj = Soul.objects.get(id=id)
        return obj       
        
    def get(self, request, id):
        try:
            if not self.query_set(request, id).won_by == self.request.user:
                return Response({"error":"You don't have permission to view this record"}, status=status.HTTP_401_UNAUTHORIZED)
            else:
                obj = self.query_set(request, id)
                serializer = self.serializer_class(obj)
                return Response(serializer.data, status=status.HTTP_200_OK)
        except:
            return Response({'error': 'Soul record not found'}, status=status.HTTP_404_NOT_FOUND)

        
    def put(self, request, id):
        try:
            if not self.query_set(request, id).won_by == self.request.user:
                return Response({"error":"You don't have permission to view this record"}, status=status.HTTP_401_UNAUTHORIZED)
            
            else:
                obj = self.query_set(request, id)
                serializer = self.serializer_class(obj, data=request.data)
                serializer.is_valid(raise_exception=True)
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
        except:
            return Response({'error': 'Soul record not found'}, status=status.HTTP_404_NOT_FOUND)
    
    def delete(self, request, id):
        try:
            if not Soul.objects.get(id=id).won_by == self.request.user:
                return Response({"error":"You don't have permission to view this record"}, status=status.HTTP_401_UNAUTHORIZED)
            
            else:
                self.query_set(request, id).delete()
                return Response("Deleted", status=status.HTTP_204_NO_CONTENT)
        except:
            return Response({'error': 'soul record not found'}, status=status.HTTP_404_NOT_FOUND)

class Get_All_Souls(generics.GenericAPIView):
    serializer_class = SoulSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        obj = Soul.objects.all()
        if get_user_model().objects.get(id=self.request.user.id).role != 'Admin':
            return Response({"error":"You don't have permission to view all souls"}, status=status.HTTP_200_OK)

        else:
            serializer = self.serializer_class(obj, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
