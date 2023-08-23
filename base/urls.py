from django.urls import re_path as url
from django.db import router
from django.urls import include, path
from base.views import *
from rest_framework_swagger.views import get_swagger_view

schema_view = get_swagger_view(title='Pastebin API')

from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
# from rest_framework_simplejwt.views import TokenBlacklistView
...

schema_view = get_schema_view(
   openapi.Info(
      title="Snippets API",
      default_version='v1',
      description="Test description",
      terms_of_service="https://www.google.com/policies/terms/",
      contact=openapi.Contact(email="contact@snippets.local"),
      license=openapi.License(name="BSD License"),
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)
# router.register('question', cebula_views.SendMailAPIView, 'userpage-question')
urlpatterns = [
    # url(r'^hhh', schema_view),

    
    path('api/v1/login/',Custom_Login.as_view(),name='login'),
    path('api/v1/logout/',LogoutAPIView.as_view(),name='login'),
    path('api/v1/concurrent_login/',Concurrent_login.as_view(),name='concurrent_login'),
    path('api/v1/change_password/',ChangePasswordAPIView.as_view(),name='change_password'),
    path('api/v1/forget_password/',ResetPassword.as_view(),name='forget_password'),
    path('api/v1/profile/',Profile.as_view(),name='profile'),

   #  create for test before impliment scheduler====

    url(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    url(r'^swagger/$', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    url(r'^redoc/$', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]
