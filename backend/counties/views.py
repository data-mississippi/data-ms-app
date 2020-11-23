from rest_framework import viewsets, status
from rest_framework.response import Response
from .models import County
from .serializers import CountySerializer

class CountyViewSet(viewsets.ModelViewSet):
	"""Returns name and FIPS code for all counties."""
	queryset = County.objects.exclude(pk='000')
	serializer_class = CountySerializer
	http_method_names = ['get']