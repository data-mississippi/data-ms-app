from rest_framework import serializers
from .models import County, CountyBorderGeoJSON, VotingPrecinct, Population

class CountySerializer(serializers.HyperlinkedModelSerializer):
	class Meta:
		model = County
		fields = ['fips', 'name']


class CountyBorderSerializer(serializers.ModelSerializer):
	county_fips = serializers.CharField(source='county.fips', read_only=True)
	
	class Meta:
		model = CountyBorderGeoJSON
		fields = ['county_fips', 'geojson']


class VotingPrecinctSerializer(serializers.ModelSerializer):
	county_fips = serializers.CharField(source='county.fips', read_only=True)

	class Meta:
		model = VotingPrecinct
		fields = ['county_fips', 'geojson', 'name', 'voting_district_code', 'name_area_description']


class PopulationSerializer(serializers.ModelSerializer):
	county_fips = serializers.CharField(source='county.fips', read_only=True)

	class Meta:
		model = Population
		fields = '__all__'
