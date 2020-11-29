from csv import reader
from counties.models import County, CountyGeoJSON, CountyPrecinctGeoJSON
import sys
import os
import string
import re

# import fips and county name for each county
with open('counties/ms-fips.csv', 'r') as f:
	csv_reader = reader(f)
	counter = 0
	header = ['state', 'state_fips', 'county_fips', 'county_name', 'fips_class']
	counties = []
	for row in csv_reader:
		row_dict = {}
		for index, column in enumerate(row):
			key = header[index]
			print(key)
			row_dict.update({key: column})
		print(row_dict)
		counties.append(row_dict)
	print(counties)
	for county in counties:
		print('bouta save this county')
		print(county)
		county_name = re.sub(r'^ County$', '', county['county_name'])
		county_name
		c = County(
			fips=county['county_fips'],
			name=county['county_name'].replace(' County', ''),
			state=county['state'],
			state_fips=county['state_fips'],
			fips_class=county['fips_class']
			)
		c.save()
	print('something good happened')


# import geojson for all the counties
import json
import pprint
with open ('counties/scripts/ms-counties.json') as json_file:
	ms = County.objects.get(pk='000')
	data = json.load(json_file)
	ms_geo_json = CountyGeoJSON(county=ms, geojson=data)
	ms_geo_json.save()
	print('ms geojson saved')


# {"type":"FeatureCollection", "features": []}
# "properties":{"STATEFP10":"28","COUNTYFP10":"081","VTDST10":"203","GEOID10":"28081203","VTDI10":"A","NAME10":"Euclautubba","NAMELSAD10":"Euclautubba Voting District","LSAD10":"V2","MTFCC10":"G5240","FUNCSTAT10":"N","ALAND10":15410331,"AWATER10":0,"INTPTLAT10":"+34.4085819","INTPTLON10":"-088.7274251"}

with open ('counties/scripts/ms-counties.json') as json_file:
	data = json.load(json_file)
	for feature in data.get('features'):
		geo_dict = {
		'type': 'FeatureCollection',
		'features': []
		}
		geo_dict.get('features').append(feature)
		print(feature.get('properties'))
		county_fips = feature['properties']['CNTY_FIPS']
		print(county_fips)
		c = County.objects.get(pk=county_fips)
		print(c.fips)
		county_geo_json = CountyGeoJSON(county=c, geojson=geo_dict)
		county_geo_json.save()
	print('saved them all')
		

with open ('counties/scripts/ms-precincts-12.json') as json_file:
	data = json.load(json_file)
	for feature in data.get('features'):
		print(feature.get('properties'))
		geo_dict = {
		'type': 'FeatureCollection',
		'features': []
		}
		geo_dict.get('features').append(feature)
		county_fips = feature['properties']['COUNTYFP10']
		c = County.objects.get(pk=county_fips)
		county_geo_json = CountyPrecinctGeoJSON(county=c, geojson=geo_dict)
		county_geo_json.save()