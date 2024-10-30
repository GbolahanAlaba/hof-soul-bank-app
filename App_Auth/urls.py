from django.urls import path, include
from . import views
from . views import *
from knox import views as knox_views


#  SWAGGER
from django.urls import re_path
from rest_framework import permissions




urlpatterns = [
   path('signin/', AuthViewSets.as_view({"post": "signin"}), name='signin'),
   path('signup/', AuthViewSets.as_view({"post": "signup"}), name='signup'),

]