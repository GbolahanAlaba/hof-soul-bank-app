from django.urls import path, include
from . import views
from . views import *
from knox import views as knox_views


#  SWAGGER
from django.urls import re_path
from rest_framework import permissions




urlpatterns = [
   path('create-auth/', SetupViewSets.as_view({"post": "create_auth_code"}), name='auth-create'),
   path('create-team/', SetupViewSets.as_view({"post": "create_team"}), name='team-create'),
   path('create-sector/', SetupViewSets.as_view({"post": "create_sector"}), name='sector-create'),

]