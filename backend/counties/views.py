from django.http import HttpResponse, JsonResponse
from rest_framework import viewsets, status
from rest_framework.response import Response
from .models import County, CountyGeoJSON
from .serializers import CountySerializer, CountyGeoJSONSerializer

class CountyViewSet(viewsets.ModelViewSet):
	"""Returns name and FIPS code for all counties."""
	queryset = County.objects.exclude(pk='000')
	serializer_class = CountySerializer
	http_method_names = ['get']


def county_geo_json_list(request):
	print('getting them all')
	if request.method == 'GET':
		geos = CountyGeoJSON.objects.all()
		serializer = CountyGeoJSONSerializer(geos, many=True, context={'request': request})
		return JsonResponse(serializer.data, safe=False)


def county_geo_json_detail(request, fips):
	print()
	print('request')
	print(fips)
	try:
		print('trying this')
		county_geo = CountyGeoJSON.objects.filter(county__pk=fips)
		print('got this')
		print(county_geo)
	except CountyGeoJSON.DoesNotExist:
		return HttpResponse(status=404)

	if request.method == 'GET':
		serializer = CountyGeoJSONSerializer(county_geo[0], context={'request': request})
		return JsonResponse(serializer.data)
