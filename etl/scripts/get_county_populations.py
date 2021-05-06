import sys
import re
import json
import os
from dataclasses import asdict
from survey import Survey
from ms_census import MississippiCensus


print('target')

target = sys.argv[2]
print(target)
print(sys.argv[1])
print(sys.argv[0])
api_key = os.getenv('CENSUS_API_KEY')

sf1 = Survey(
    survey_key='sf1',
    dataset_name='Census Summary File 1',
    description='Population by Race',
    year=2010,
    variable_key='P3',
    lookup_key='group(P3)',
    exclude=['P003001ERR']
)

acs5 = Survey(
    survey_key='acs5',
    dataset_name='American Community Survey 5-Year Data (2009-2019)',
    description='Population by Race',
    year=2019,
    variable_key='B02001',
    lookup_key='group(B02001)',
    variable_ends_with='E',
    exclude=['B02001_009E', 'B02001_010E']
)

surveys = [sf1, acs5]

c = MississippiCensus(api_key)

for s in surveys:
    # get the key for the survey and access that survey's 
    # census client based on the survey key, i.e. acs5 or sf1
    survey_client = getattr(c, s.survey_key)

    variables = c.get_variables(survey_client, s)

    # parse out the variable names and add them to our data object, so that 
    # we have the key/value with the proper name for the key
    for variable, metadata in variables.items():
        label = metadata['label']

        if s.variable_ends_with and \
           not variable.endswith(s.variable_ends_with):
            continue
        
        if variable in s.exclude:
            continue
        
        remove = '^(Total!!)|(Estimate!!Total!!)|(Estimate!!)|alone'

        formatted_label = re.sub(remove, '', label).strip().upper()

        s.labels[variable] = formatted_label

    data_rows = survey_client.get(s.lookup_key, geo={'for': 'county:*', 'in': 'state:28'})

    for county_data in data_rows:
        county = {'fips': county_data['county']}
        
        for variable, label in s.labels.items():
            population = county_data[variable]
            county[label] = population
            
            s.rows.append(county)

output_data = [asdict(d) for d in surveys]

with open(target, 'w') as f:
    f.write(json.dumps(output_data, indent=4))

# TODO stdout
