import sys
import re
import json
import os
from dataclasses import asdict
from survey import Survey
from ms_census import MississippiCensus

sf1 = Survey(
    survey_key='sf1',
    dataset_name='Census Summary File 1',
    description='Total Population',
    year=2010,
    variable_key='P1',
    lookup_key='group(P1)',
    exclude=['P001001ERR']
)

surveys = [sf1]

api_key = os.getenv('CENSUS_API_KEY')
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

        remove = r'^(Total!!)|(Estimate!!Total:!!)|(Estimate!!Total!!)|(Estimate!!)|alone'
        formatted_label = re.sub(remove, '', label).strip().upper().replace(' ', '_')

        s.labels[variable] = label

   
    data_rows = survey_client.get(s.lookup_key, geo={'for': 'county:*', 'in': 'state:28'})

    for county_data in data_rows:
        county = {'fips': county_data['county']}
        
        for variable, label in s.labels.items():
            population = county_data[variable]
            county[label] = population

        s.rows.append(county)

output_data = [asdict(d) for d in surveys]

json.dump(output_data, sys.stdout, indent=4)
