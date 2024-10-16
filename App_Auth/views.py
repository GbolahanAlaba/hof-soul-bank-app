from . models import *
from django.contrib.auth import get_user_model
from rest_framework.response import Response
from rest_framework import generics
from rest_framework import viewsets, permissions
from rest_framework import status
from rest_framework.authtoken.serializers import AuthTokenSerializer
from knox.auth import TokenAuthentication
from rest_framework.views import APIView
from knox.auth import AuthToken
from rest_framework.permissions import IsAuthenticated
from . serializers import *
from . utils import *
from django.db.models import Q
from rest_framework.decorators import action



class SetupViewSets(viewsets.ViewSet):
    authentication_classes=[TokenAuthentication]
    permission_classes=[IsAuthenticated]

    @handle_exeptions
    def create_auth_code(self, request):
        user = request.user

        if user.role != "Sector Leader":
            return Response({"status": "failed", "message": "Unauthorized"}, status=status.HTTP_403_FORBIDDEN)
        else:
            auth = {'hof': 'HOF'}
            auth_code = "{}{}".format(auth ['hof'], randint(100000, 999999))
            AuthCode.objects.create(auth_code=auth_code)
            return Response({"status": "success", "message": f"Authorization code created '{auth_code}'", "data": auth_code}, status=status.HTTP_201_CREATED)
    

    @handle_exeptions
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
        
    @handle_exeptions
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

class AuthViewSets(viewsets.ViewSet):
    serializer_class = AuthTokenSerializer         

    @handle_exeptions
    @action(detail=False, methods=['post'])
    def signin(self, request):
        email_or_phone = request.data['email_or_phone']
        checkUser = User.objects.filter(Q(email=email_or_phone) | Q(phone=email_or_phone)).first()

        if checkUser is None:
            return Response({"status": "failed", "message": "User not found"}, status=status.HTTP_404_NOT_FOUND)
        elif not checkUser.is_active:
            return Response({"status": "failed", "message": "Account is not verified"}, status=status.HTTP_403_FORBIDDEN)
        
        else:
            serializer = AuthTokenSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            user = serializer.validated_data["user"]
            user.last_login = timezone.now()
            user.save(update_fields=["last_login"])
            _, token = AuthToken.objects.create(user)   

            response_data = {
                "status": "success",
                "message": "Signed successfully",
                "data":{
                    "user_id": user.user_id,
                    "first_name": user.first_name,
                    "last_name": user.last_name,
                    "email": user.email,
                    "phone": user.phone,
                    'team': user.team,
                    'role': user.role,
                    'sector': user.sector,
                },
            "token": token
            }
            if user.profile_image:
                response_data['profile_image_url'] = request.build_absolute_uri(user.profile_image.url)
            return Response(response_data, status=status.HTTP_200_OK)
    

    @handle_exeptions
    @action(detail=False, methods=['post'])
    def signup(self, request, *args, **kwargs):
        # phone = request.data['phone']
        # auth_code = request.data['auth_code']
        
            
        is_valid_phone(request.data.get('phone'))   
        serializer = SignupSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        _, token = AuthToken.objects.create(user)
    
        return Response({
            "status": "success",
            "message": "Signup successful",
            "data": {
                'user_id': user.user_id,
                'first_name': user.first_name,
                'last_name': user.last_name,
                'phone': user.phone,
                'email': user.email,
                "gender": user.gender,
                'sector': user.sector,
            },
        # 'token': token
        }, status=status.HTTP_201_CREATED)




 # if not AuthCode.objects.filter(auth_code=auth_code):
        #     return Response({"status": "failed", "message": "Invalid auth_code"}, status=status.HTTP_401_UNAUTHORIZED)
        # elif not is_valid_email(email):
        #     return Response({"status": "failed", "message": "Invalid email"}, status=status.HTTP_401_UNAUTHORIZED)
        # elif User.objects.filter(email=email):
        #     return Response({"status": "failed", "message": "Email exist"}, status=status.HTTP_401_UNAUTHORIZED)
        # elif User.objects.filter(phone=phone):
        #     return Response({"status": "failed", "message": "Phone number exist"}, status=status.HTTP_401_UNAUTHORIZED)
        # else:   




# Create your views here.
# @action(detail=False, methods=['post'], authentication_classes=[TokenAuthentication], permission_classes=[IsAuthenticated])
# class CreateAuthCode(generics.GenericAPIView):
#     serializer_class = AuthCodeSerializer
#     authentication_classes = [TokenAuthentication]
#     permission_classes = [IsAuthenticated]

#     def post(self, request):
#         auth_user = User.objects.get(id=self.request.user.id)

#         if auth_user.role != 'Admin' and auth_user.role != 'Sector Leader':
#             return Response({"error": "You don't have access to generate authentication code"}, status=status.HTTP_401_UNAUTHORIZED)
#         else:
#             auth = {'hof': 'HOF'}
#             auth_key = "{}{}".format(auth ['hof'], randint(100000, 999999))
#             serializer = self.serializer_class(data=request.data)
#             serializer.is_valid(raise_exception=True)
#             saveauth = serializer.save()
#             saveauth.auth_code = auth_key
#             saveauth.save()
#             return Response({'This is your code %s'%(auth_key)}, status=status.HTTP_201_CREATED)

# class Create_Sector(generics.GenericAPIView):
#     serializer_class = SectorSerializer
#     authentication_classes = [TokenAuthentication]
#     permission_classes = [IsAuthenticated]
    
#     def post(self, request, *args, **kwargs):
#         if get_user_model().objects.get(id=self.request.user.id).role != 'Admin':
#             return Response({"error":"You don't have permission to create sector"}, status=status.HTTP_401_UNAUTHORIZED)
#         else:            
#             serializer = self.serializer_class(data=request.data)
#             serializer.is_valid(raise_exception=True)
#             serializer.save(created_by=self.request.user)
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
        
# class Create_Role(generics.GenericAPIView):
#     serializer_class = RoleSerializer
#     authentication_classes = [TokenAuthentication]
#     permission_classes = [IsAuthenticated]
    
#     def post(self, request, *args, **kwargs):
#         if get_user_model().objects.get(id=self.request.user.id).role != 'Admin':
#             return Response({"error":"You don't have permission to create role"}, status=status.HTTP_401_UNAUTHORIZED)
#         else:            
#             serializer = self.serializer_class(data=request.data)
#             serializer.is_valid(raise_exception=True)
#             serializer.save(created_by=self.request.user)
#             return Response(serializer.data, status=status.HTTP_201_CREATED)

# class Update_Role(generics.GenericAPIView):
#     serializer_class = RoleSerializer
#     authentication_classes = [TokenAuthentication]
#     permission_classes = [IsAuthenticated]

#     def get(self, request, id):
#         if get_user_model().objects.get(id=self.request.user.id).role != 'Admin':
#             return Response({"error":"You don't have permission to view role"}, status=status.HTTP_401_UNAUTHORIZED)
        
#         try:
#             obj = Roles.objects.get(id=id)
#         except:
#             return Response({"error":"User not found"}, status=status.HTTP_404_NOT_FOUND)

#         else:
#             serializer = self.serializer_class(obj)
#             return Response(serializer.data, status=status.HTTP_200_OK)
    
#     def put(self, request, id):
#         if get_user_model().objects.get(id=self.request.user.id).role != 'Admin':
#             return Response({"error":"You don't have permission to view role"}, status=status.HTTP_401_UNAUTHORIZED)
        
#         try:
#             obj = Roles.objects.get(id=id)
#         except:
#             return Response({"error":"User not found"}, status=status.HTTP_404_NOT_FOUND)
        
#         else:            
#             serializer = self.serializer_class(obj, data=request.data)
#             serializer.is_valid(raise_exception=True)
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
    
#     def delete(self, request, id):
#         if get_user_model().objects.get(id=self.request.user.id).role != 'Admin':
#             return Response({"error":"You don't have permission to view role"}, status=status.HTTP_401_UNAUTHORIZED)
        
#         try:
#             obj = Roles.objects.get(id=id)
#         except:
#             return Response({"error":"User not found"}, status=status.HTTP_404_NOT_FOUND)

#         obj.delete()
#         return Response("Deleted", status=status.HTTP_204_NO_CONTENT)

# class Update_Sector(generics.GenericAPIView):
#     serializer_class = SectorSerializer
#     authentication_classes = [TokenAuthentication]
#     permission_classes = [IsAuthenticated]

#     def get(self, request, id):
#         if get_user_model().objects.get(id=self.request.user.id).role != 'Admin':
#             return Response({"error":"You don't have permission to view role"}, status=status.HTTP_401_UNAUTHORIZED)
        
#         try:
#             obj = Sectors.objects.get(id=id)
#         except:
#             return Response({"error":"User not found"}, status=status.HTTP_404_NOT_FOUND)

#         else:
#             serializer = self.serializer_class(obj)
#             return Response(serializer.data, status=status.HTTP_200_OK)
    
#     def put(self, request, id):
#         if get_user_model().objects.get(id=self.request.user.id).role != 'Admin':
#             return Response({"error":"You don't have permission to view role"}, status=status.HTTP_401_UNAUTHORIZED)
        
#         try:
#             obj = Sectors.objects.get(id=id)
#         except:
#             return Response({"error":"User not found"}, status=status.HTTP_404_NOT_FOUND)
        
#         else:            
#             serializer = self.serializer_class(obj, data=request.data)
#             serializer.is_valid(raise_exception=True)
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
    
#     def delete(self, request, id):
#         if get_user_model().objects.get(id=self.request.user.id).role != 'Admin':
#             return Response({"error":"You don't have permission to view role"}, status=status.HTTP_401_UNAUTHORIZED)
        
#         try:
#             obj = Sectors.objects.get(id=id)
#         except:
#             return Response({"error":"User not found"}, status=status.HTTP_404_NOT_FOUND)

#         obj.delete()
#         return Response("Deleted", status=status.HTTP_204_NO_CONTENT)
