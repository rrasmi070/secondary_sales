"""secondary_sales URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
    
    
"""

from django.contrib import admin
from django.urls import path,include
from django.conf.urls import url
from rest_framework_simplejwt import views as jwt_views
from django.conf.urls.static import static
from django.conf import settings

from base.views import UserRefreshTokenGeneratorGenerics,custom404,main_home
import requests
import debug_toolbar


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('base.urls')),
    path('', include('master.urls')),
    path('', include('wd.urls')),
    path('', include('branch_user.urls')),
    path('', include('ss_admin.urls')),
    path('api/token/refresh/',UserRefreshTokenGeneratorGenerics.as_view(),name='token_refresh'),
    # path('api/token/refresh/', jwt_views.TokenRefreshView.as_view(), name='token_refresh'),
    # path('', include('manager.urls')),
    url(r'^.*/$',custom404,name='error404'),
    path('', main_home, name='home'),
    path('__debug__/', include(debug_toolbar.urls)),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)



if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)