from django.urls import path, include
from . import views
from . views import *
from knox import views as knox_views


#  SWAGGER
from django.urls import re_path
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi


schema_view = get_schema_view(
   openapi.Info(
      title="Soul Bank API",
      default_version='v1',
      description="This is HOF Soul Bank App API Doc",
      terms_of_service="https://www.google.com/policies/terms/",
      contact=openapi.Contact(email="jedida@gmail.com"),
      license=openapi.License(name="BSD License"),
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)


urlpatterns = [
   path('create_soul/', Create_Soul.as_view(), name='create_soul'), # create soul
   path('get_user_souls/', Get_User_Souls.as_view(), name='get_user_souls'), # get soul
   path('update_user_soul/<str:id>/', Update_User_Soul.as_view(), name='update_user_soul'), # update user soul
   path('get_all_souls/', Get_All_Souls.as_view(), name='get_all_souls'), # get soul

   path('swagger<format>/', schema_view.without_ui(cache_timeout=0), name='schema-json'),
   path('go/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
   path('', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),

]