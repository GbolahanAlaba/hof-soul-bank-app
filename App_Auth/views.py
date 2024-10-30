from . models import *
from App_Users.models import *
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
from . serializers import *
from . utils import *
from django.db.models import Q
from rest_framework.decorators import action



class AuthViewSets(viewsets.ViewSet):
    serializer_class = AuthTokenSerializer         

    @handle_exceptions
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

            refresh = RefreshToken.for_user(user)  # This will create the JWT refresh and access tokens
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
            "tokens": {
                    "access": str(refresh.access_token),  # Return the access token
                    "refresh": str(refresh),  # Return the refresh token
                }
            }
            if user.profile_image:
                response_data['profile_image_url'] = request.build_absolute_uri(user.profile_image.url)
            return Response(response_data, status=status.HTTP_200_OK)
    

    @handle_exceptions
    @action(detail=False, methods=['post'])
    def signup(self, request, *args, **kwargs):
        # auth_code = request.data['auth_code']
        
        is_valid_phone(request.data.get('phone'))
        validate_auth_code(request.data.get('auth_code'))  
        serializer = SignupSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        Role.objects.create(user=user)
    
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
