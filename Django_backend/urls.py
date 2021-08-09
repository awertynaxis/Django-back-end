
"""Django_backend URL Configuration

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
from django.urls import path, include, re_path
from rest_framework.schemas import get_schema_view
from rest_framework_swagger.views import get_swagger_view

def trigger_error(request):
    division_by_zero = 1 / 0

swagger_view = get_schema_view(title='Django_backend API')
schema_view = get_swagger_view(title=' Django_backend API')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('master/', include('master.urls')),
    path('client/', include('client.urls')),
    path('order/', include('order.urls')),
    path('schedule/', include('schedule.urls')),
    path('docs/', swagger_view),
    path('superswagger/', schema_view),
    path('sentry-debug/', trigger_error),
]
