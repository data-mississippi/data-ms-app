from rest_framework import serializers
from .models import County, CountyBorderGeoJSON

class CountySerializer(serializers.HyperlinkedModelSerializer):
	class Meta:
		model = County
		fields = ['fips', 'name']

class CountyBorderSerializer(serializers.ModelSerializer):
	county_fips = serializers.CharField(source='county.fips', read_only=True)
	
	class Meta:
		model = CountyBorderGeoJSON
		fields = ['county_fips', 'geojson']