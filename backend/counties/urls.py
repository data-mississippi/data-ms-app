from django.urls import path, include
from rest_framework import routers
from . import views

router = routers.DefaultRouter()
router.register(r'', views.CountyViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('geojson/borders/', views.CountyBorderList.as_view()),
    path('<str:county>/geojson/borders/', views.CountyBorderDetail.as_view()),
]