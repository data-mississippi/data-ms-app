import requests
from census import Census

class MississippiCensus(Census):

    def get_variables(self, survey_client, survey):
        # need to know some details about the data we're gonna get
        tables_metadata = survey_client.tables(year=int(survey.year))

        # get the desired url for the table we want, from the tables' metadata
        variable_target_url, = [f for f in tables_metadata if f['name'] == survey.variable_key]
        # get the variables for the table we want
        variables = requests.get(variable_target_url['variables']).json()['variables']
        
        return variables
