from django.urls import path, include
from rest_framework import routers
from . import views

router = routers.DefaultRouter()
router.register(r'', views.CountyViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('borders/', views.CountyBorderList.as_view()),
    path('borders/<str:county>/', views.CountyBorderDetail.as_view()),
    path('precincts/', views.VotingPrecinctList.as_view()),
    path('precincts/<str:county>/', views.get_all_precincts_for_county)
]
