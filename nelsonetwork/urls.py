"""
URL configuration for nelsonetwork project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from django.urls import path, include
from rest_framework import routers
from nelsonetworkapi.views.auth import check_user, register_user
from nelsonetworkapi.views import UserView, NetworkView, DeviceView, NetworkDeviceView, DocumentationView

# Initialize router
router = routers.DefaultRouter(trailing_slash=False)
router.register(r'users', UserView, 'user')
router.register(r'networks', NetworkView, 'network')
router.register(r'devices', DeviceView, 'device')
router.register(r'networkdevices', NetworkDeviceView, 'networkdevice')
router.register(r'documentations', DocumentationView, 'documentation')




# Define URL patterns
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include(router.urls)),  # Include router-generated URLs
    path('checkuser/', check_user, name='check_user'),  # Custom endpoint
    path('registeruser/', register_user, name='register_user'),  # Custom endpoint
]
