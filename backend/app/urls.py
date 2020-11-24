"""app URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
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
from django.urls import path, re_path, include
from django.views.generic import TemplateView
from rest_framework import routers
from rest_framework.schemas import get_schema_view
from counties import views #CountyViewSet, county_geo_json_list, county_geo_json_detail

router = routers.DefaultRouter()
# router.register(r'counties', CountyViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('geo/', views.county_geo_json_list),
    path('geo/<str:fips>/', views.county_geo_json_detail),
    path('docs', get_schema_view(
        title='Data Mississippi',
        description='An API about Mississippi.',
        version='0.1'
    ), name='openapi-schema'),
    path('admin/', admin.site.urls),
    re_path(".*", TemplateView.as_view(template_name="index.html"))
]
