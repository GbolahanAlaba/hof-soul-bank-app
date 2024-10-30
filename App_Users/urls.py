from django.urls import path
from . views import *




urlpatterns = [
   path('create-auth/', SetupViewSets.as_view({"post": "create_auth_code"}), name='auth-create'),
   path('create-team/', SetupViewSets.as_view({"post": "create_team"}), name='team-create'),
   path('create-sector/', SetupViewSets.as_view({"post": "create_sector"}), name='sector-create'),

]