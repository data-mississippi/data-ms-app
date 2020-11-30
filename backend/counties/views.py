from django.http import HttpResponse, JsonResponse
from rest_framework import viewsets, status, generics
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import County, CountyBorderGeoJSON
from .serializers import CountySerializer, CountyBorderSerializer


class CountyViewSet(viewsets.ModelViewSet):
	"""
	Returns name and FIPS code for all counties.
	"""
	queryset = County.objects.exclude(pk='000')
	serializer_class = CountySerializer
	http_method_names = ['get']


class CountyBorderList(generics.ListAPIView):
	"""
	Returns GeoJSON of all county borders.
	"""
	queryset = CountyBorderGeoJSON.objects.all()
	serializer_class = CountyBorderSerializer


class CountyBorderDetail(generics.RetrieveAPIView):
	"""
	Returns GeoJSON for a single county's border. 
	The object is queried by the county's FIPS.
	"""
	queryset = CountyBorderGeoJSON.objects.all()
	serializer_class = CountyBorderSerializer
	lookup_field = 'county'