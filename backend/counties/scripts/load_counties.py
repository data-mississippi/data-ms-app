from csv import reader
from counties.models import County, CountyGeoJSON
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
	pprint.pprint(data)
	ms_geo_json = CountyGeoJSON(county=ms)