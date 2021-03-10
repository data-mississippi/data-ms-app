import sys
import csv
import re
import json
from pprint import pprint
import requests

# print(sys.argv)
# fips_path = sys.argv[1]
target = sys.argv[2]




# fips_array = []
# with open(fips_path, 'r') as f:
#     reader = csv.reader(f)
#     for row in reader:
#         print('row')
#         print(row[2])
#         fips_array.append(row[2])


# url = f'https://api.census.gov/data/2010/dec/sf1?get=group(P3)&for=county:001&in=state:28'
# county = requests.get(url)

# headers_array = county.json()[0]
# headers_json = requests.get('https://api.census.gov/data/2010/dec/sf1/groups/P3.json')

# print('var')
# variables = headers_json.json()['variables']
# print(variables)
# header = ''
# print(headers_array)
# for header in headers_array:
#     print('header')
#     print(header)
#     header_name = variables.get(header, None)
#     print('heaer name')
#     print(header_name)
#     if header_name is not None:
#         header += (header_name['label'] + ',')

# print('final')
# print(header)
# # header = ','.join() + '\n'
# # print('header')
# # print(type(header))

# csv_string = ''
# csv_string += header

# print('fips array')
# print(fips_array)
# for county in fips_array:
#     url = f'https://api.census.gov/data/2010/dec/sf1?get=group(P3)&for=county:'+county+'&in=state:28'
#     county = requests.get(url)
#     print(county.json())
#     county_population = ','.join(filter(None, county.json()[1]))
#     csv_string += (county_population + '\n')

# print(csv_string)

# with open(target, 'w') as f:
#     f.write(csv_string)


from census import Census
import os
api_key = os.getenv('CENSUS_API_KEY')
c = Census(api_key)
# c.sf1.get('P016001')

#cs_tables = c.acs5.get('group(B02001)', geo={'for': 'county:*', 'in': 'state:28'})
#cs_tables = c.acs5.tables()
#pprint(cs_tables)

#shttps://www.census.gov/programs-surveys/acs/guidance/handbooks/summary-file.html
# https://api.census.gov/data/2019/acs/acs5.html
# https://www.census.gov/programs-surveys/acs/guidance/estimates.html

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
        'label_ends_with': None,
        'rows': []
    },
    {
        'dataset_key': 'acs5',
        'dataset_name': 'American Community Survey 5-Year Data (2009-2019)',
        'description': 'Population by Race',
        'year': '2019', #TODO: year for acs5 ?
        'survey_key': 'B02001',
        'lookup_key': 'group(B02001)',
        'labels': [],
        'label_ends_with': 'E',
        #'label_regex': 'E$', # get the population estimations, no margin of error or annotations
        'rows': [],
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
    for index, value in enumerate(variables['variables']):
        label_name = variables['variables'][value].get('label', None)

        # terrible way of parsing out the estimate for acs5
        if data['label_ends_with'] is not None and value.endswith(data['label_ends_with']) == False:
            label_name = None

        if label_name is not None:
            data['labels'].append({
                value: re.sub('^(Total!!)|(Estimate!!Total!!)|(Estimate!!)|alone', '', label_name).strip()
            })
    print('data')
    pprint(data)

    data_rows = census_client.get(data['lookup_key'], geo={'for': 'county:*', 'in': 'state:28'})

    for county_data in data_rows:
        county = {
            'fips': county_data['county']
        }

        for key, label in enumerate(data['labels']):
            label_name = list(label.keys())[0]

            population = county_data.get(label_name)

            county.update({
                label_name: population
            })

            data['rows'].append(county)

# print('final data !!')
# pprint(datasets)


with open(target, 'w') as f:
    f.write(json.dumps(datasets))