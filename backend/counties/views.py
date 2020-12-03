from django.http import HttpResponse, JsonResponse
from rest_framework import viewsets, status, generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .models import County, CountyBorderGeoJSON, VotingPrecinct
from .serializers import CountySerializer, CountyBorderSerializer, VotingPrecinctSerializer


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


class VotingPrecinctList(generics.ListAPIView):
	"""
	Returns all voting precincts for the state.
	"""
	print('voting precinct list')
	queryset = VotingPrecinct.objects.all()
	serializer_class = VotingPrecinctSerializer


@api_view(['GET'])
def get_all_precincts_for_county(request, county):
	try:
		county_precincts = VotingPrecinct.objects.filter(county__pk=county)
		if request.method == 'GET':
			serializer = VotingPrecinctSerializer(county_precincts, context={'request': request}, many=True)
			return Response(serializer.data)
	except VotingPrecinct.DoesNotExist:
		return HttpResponse(status=404)