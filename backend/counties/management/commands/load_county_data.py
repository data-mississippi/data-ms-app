import json
import re
from csv import reader
from django.core.management.base import BaseCommand 
from ...models import County, CountyBorderGeoJSON, VotingPrecinctGeoJSON, VotingPrecinct, Population


class Command(BaseCommand):
    help = 'Loads data for all counties and voting precincts.'
    
    def add_arguments(self, parser):
        parser.add_argument('--table', dest='table')
        parser.add_argument('--input', help='input path')


    def handle(self, *args, **options):
        table = options['table']
        input = options['input']

        if table == 'county':
            County.objects.all().delete()
            
            # Creates every county with the FIPS code
            with open(input, 'r') as f:
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
                    c = County(fips=county['county_fips'],
                               name=county['county_name'].replace(' County', ''),
                               state=county['state'],
                               state_fips=county['state_fips'],
                               fips_class=county['fips_class'])
                    c.save()
                    counter += 1
                self.stdout.write(self.style.SUCCESS(f'You loaded all {counter} counties into Mississippi !\n'))
            
        if table == 'borders':
            CountyBorderGeoJSON.objects.all().delete()
            # Creates a GeoJSON FeatureCollection, for each county's border
            with open (input) as json_file:
                data = json.load(json_file)
                
                # create a single MS county to query the entire map
                ms, _ = County.objects.get_or_create(pk='000')
                ms_geo_json = CountyBorderGeoJSON(county=ms, geojson=data)
                ms_geo_json.save()
                
                # parse out the geojson for each county,
                # and create a geojson feature for the county
                for feature in data.get('features'):
                    geo_dict = {
                    'type': 'FeatureCollection',
                    'features': []
                    }
                    geo_dict.get('features').append(feature)
                    county_fips = feature['properties']['COUNTYFP20']
                    c = County.objects.get(pk=county_fips)
                    county_geo_json = CountyBorderGeoJSON(county=c, geojson=geo_dict)
                    county_geo_json.save()
                self.stdout.write(self.style.SUCCESS('Saved GeoJSON for all of the county borders.\n'))
                
        if table == 'population':
            Population.objects.all().delete()
            
            with open(input) as file:
                population_surveys = json.load(file)
                
                for survey in population_surveys:
                    for row in survey['rows']:
                        county = County.objects.get(pk=row['fips'])
                        population = Population.objects.create(
                            survey=survey['survey_key'],
                            year=survey['year'],
                            county=county,
                            total=row['Total'],
                        )
                self.stdout.write(self.style.SUCCESS('Loaded population!'))
                
                
        # TODO: fix voting precinct geojson structure...
        # this data is not useful as it stands
        if table == 'precincts':
            VotingPrecinctGeoJSON.objects.all().delete()
            VotingPrecinct.objects.all().delete()

            # create voting precincts and the geojson for the precincts
            with open(input) as json_file:
                data = json.load(json_file)
                year = data.get('name')[-2:]

                # create a single MS precinct to query the entire map
                # this needs to change...leftovers from when i was learning
                ms, _ = County.objects.get_or_create(pk='000')
                ms_precinct = VotingPrecinct.objects.create(county=ms,
                                                            geojson=data)
                
                for feature in data.get('features'):
                    fip_key = f'COUNTYFP{year}'
                    county_fips = feature['properties'][fip_key]
                    if county_fips:
                        geo_dict = {
                        'type': 'FeatureCollection',
                        'features': []
                        }
                        geo_dict.get('features').append(feature)
                        
                        district_code_key = f'VTDST{year}'
                        name_key = f'NAME{year}'
                        name_area_desc_key = f'NAMELSAD{year}'
                        new_voting_precinct = VotingPrecinct(
                            voting_district_code=feature['properties'][district_code_key],
                            county=County.objects.get(pk=county_fips),
                            geojson=geo_dict,
                            name=feature['properties'][name_key],
                            name_area_description=feature['properties'][name_area_desc_key],
                        )
                        new_voting_precinct.save()
                        
                        county_geo_json = VotingPrecinctGeoJSON(precinct=new_voting_precinct, geojson=geo_dict)
                        county_geo_json.save()
                        
            self.stdout.write(self.style.SUCCESS('Loaded GeoJSON for the voting precincts!\n'))
