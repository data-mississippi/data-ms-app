from rest_framework import serializers
from .models import County, CountyGeoJSON

class CountySerializer(serializers.HyperlinkedModelSerializer):
	class Meta:
		model = County
		fields = ['fips', 'name']

class CountyGeoJSONSerializer(serializers.ModelSerializer):
	county_fips = serializers.CharField(source='county.fips', read_only=True)
	class Meta:
		model = CountyGeoJSON
		fields = ['id', 'county_fips', 'geojson']