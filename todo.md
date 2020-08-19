* [web scrape here](https://en.wikipedia.org/wiki/List_of_counties_in_Mississippi) to populate initial county table
  - scrape the wiki page to write basic county info to the counties (fips and name)
  - create a city (must exist to create the county)
  - create the population record for each county, which creates a source
  - fill in rest of county info


- where to put sources?
backend
|
|__app
|
|__population_and_demographics
|  |
|  |__models
        counties
        counties_population
        cities
        cities_population

# models

## counties
fips_code(pk),name,established_date,seats(array of city_pk),land_area,postgis_coordinates(shape files?),smithsonian_trimonial,source_pk
has many cities

## county_population
county_pk,population_count,source_pk
  - must have a source created at the same time

## source (reference? citation?)
pk,title,date_accessed,date_published,original_location,archive_location

## cities
name,county_pk,population
has many counties
https://docs.djangoproject.com/en/3.0/topics/db/models/#s-many-to-many-relationships
https://en.wikipedia.org/wiki/List_of_U.S._municipalities_in_multiple_counties#Mississippi


## demographics?

census blocks
state > county > county subdivision > tract > block group > blocks

https://www.its.ms.gov/Procurement/Documents/ISS%20Procurement%20Manual.pdf#page=155

https://www.mdah.ms.gov/
http://zed.mdah.state.ms.us/
http://da.mdah.ms.gov/browse-all
http://www.transparency.ms.gov/
https://www.ms.gov/government/agency-directory
https://www.its.ms.gov
https://www.ms.gov/its/public_record_request
https://www.gis.ms.gov/
wtf? https://www.giscouncil.ms.gov/

ui
https://ce.naco.org/?dset=COVID-19%20Cases&ind=Confirmed%20COVID-19%20Cases%20per%2010k%20residents
click on county and click "add to quick compare"

https://usafacts.org/visualizations/coronavirus-covid-19-spread-map/
https://budgetmodel.wharton.upenn.edu/
https://www.census.gov/data/developers/data-sets.html



postgis
http://www.smartjava.org/content/using-d3js-visualize-gis/