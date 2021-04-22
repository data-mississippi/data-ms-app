import sys
import csv
import re
import json
import os
from pprint import pprint
import requests
from census import Census

# print(sys.argv)
# fips_path = sys.argv[1]
target = sys.argv[2]

api_key = os.getenv('CENSUS_API_KEY')
c = Census(api_key)

# TODO: turn the dicts into a data class?
datasets = [
    {
        'dataset_key': 'sf1',
        'dataset_name': 'Census Summary File 1',
        'description': 'Population by Race',
        'year': '2010',
        'survey_key': 'P3',
        'lookup_key': 'group(P3)',
        'labels': [],
        'label_ends_with': False,
        'rows': [],
        'merge': False,
        'exclude': ['P003001ERR']
    },
    {
        'dataset_key': 'acs5',
        'dataset_name': 'American Community Survey 5-Year Data (2009-2019)',
        'source': 'https://api.census.gov/data/2019/acs/acs5.html',
        'description': 'Population by Race',
        'year': '2019', #TODO: year for acs5 ?
        'survey_key': 'B02001',
        'lookup_key': 'group(B02001)',
        'labels': [],
        'label_ends_with': 'E', # bad. get the population estimations, no margin of error or annotations. see https://www.census.gov/programs-surveys/acs/guidance/estimates.html
        'rows': [],
        'raw_data': [],
        'exclude': ['B02001_009E', 'B02001_010E']
    },
]

for data in datasets:
    # get the key for the survey and access that survey's 
    # census client based on the survey key, i.e. acs5 or sf1
    dataset_key = data['dataset_key']
    census_client = c.__dict__[dataset_key]

    # need to know some details about the data we're gonna get
    tables_metadata = census_client.tables()

    # get the desired url for the table we want, from the tables' metadata
    variable_target_url = [f for f in tables_metadata if f['name'] == data['survey_key']]

    # get the variables for the table we want
    variables = requests.get(variable_target_url[0]['variables']).json()

    # parse out the variable names and add them to our data object, so that 
    # we have the key/value with the proper name for the key
    for index, label_key in enumerate(variables['variables']):
        label_name = variables['variables'][label_key].get('label', None)

        # terrible way of parsing out the estimate for acs5
        if data['label_ends_with'] and label_key.endswith(data['label_ends_with']) == False:
            label_name = None

        if label_key in data['exclude']:
            label_name = None

        if label_name is not None:
            data['labels'].append({
                label_key: re.sub('^(Total!!)|(Estimate!!Total!!)|(Estimate!!)|alone', '', label_name).strip().upper()
            })

    data_rows = census_client.get(data['lookup_key'], geo={'for': 'county:*', 'in': 'state:28'})

    for county_data in data_rows:
        county = {
            'fips': county_data['county']
        }

        for key, label in enumerate(data['labels']):
            label_name = list(label.values())[0]
            label_key = list(label.keys())[0]

            population = county_data.get(label_key)

            county.update({
                label_name: population
            })

            data['rows'].append(county)

# test the totals add up
import csv
with open(target, 'w') as f:
    writer = csv.DictWriter(f, fieldnames=datasets[0]['labels'])
    writer.writeheader()
    for data in data_dict
    f.write(json.dumps(datasets))