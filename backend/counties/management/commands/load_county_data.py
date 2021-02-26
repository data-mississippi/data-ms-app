import json
import re
from csv import reader
from django.core.management.base import BaseCommand, CommandError 
from ...models import County, CountyBorderGeoJSON, VotingPrecinctGeoJSON, VotingPrecinct


class Command(BaseCommand):
    help = 'Loads data for all counties and voting precincts.'

    def handle(self, *args, **options):
        County.objects.all().delete()
        CountyBorderGeoJSON.objects.all().delete()
        VotingPrecinctGeoJSON.objects.all().delete()
        VotingPrecinct.objects.all().delete()


        # Creates every county with the FIPS code
        with open('counties/raw/ms-fips.csv', 'r') as f:
            csv_reader = reader(f)
            counter = 0
            header = ['state', 'state_fips', 'county_fips', 'county_name', 'fips_class']
            counties = []
            for row in csv_reader:
                row_dict = {}
                for index, column in enumerate(row):
                    key = header[index]
                    row_dict.update({key: column})
                counties.append(row_dict)
            for county in counties:
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
            print(f'You loaded all {counter} counties into Mississippi !')
            print()
            
        
         # Creates a GeoJSON FeatureCollection, for each county's border
        with open ('counties/raw/ms-counties.json') as json_file:
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
                county_geo_json = CountyBorderGeoJSON(county=c, geojson=geo_dict)
                county_geo_json.save()
            print('Saved GeoJSON for all of the county borders.')


        # Create a GeoJSON "County" object for the entire state
        with open ('counties/raw/ms-counties.json') as json_file:
            ms = County.objects.create(pk='000')
            data = json.load(json_file)
            ms_geo_json = CountyBorderGeoJSON(county=ms, geojson=data)
            ms_geo_json.save()
            print('Now you have a single County object that represents the entire state. It has a primary key of 000.')
            print('It exsits so that you can query a signle GeoJSON object with various lines for the entire state.')
            print('Instead of selecting all counties and then compiling the GeoJSON for the entire state')


        # create voting precincts and the geojson for the precincts
        with open ('counties/raw/ms-precincts-12.geojson') as json_file:
            data = json.load(json_file)
            for feature in data.get('features'):
                print(feature.get('properties'))
                county_fips = feature['properties']['COUNTYFP10']
                if county_fips != '':
                    geo_dict = {
                    'type': 'FeatureCollection',
                    'features': []
                    }
                    geo_dict.get('features').append(feature)
                    new_voting_precinct = VotingPrecinct(
                        voting_district_code=feature['properties']['VTDST10'],
                        county=County.objects.get(pk=county_fips),
                        geojson=geo_dict,
                        name=feature['properties']['NAME10'],
                        name_area_description=feature['properties']['NAMELSAD10'],

                    )
                    new_voting_precinct.save()
                    
                    county_geo_json = VotingPrecinctGeoJSON(precinct=new_voting_precinct, geojson=geo_dict)
                    county_geo_json.save()
