precincts : etl/output/county_precincts_2020.geojson
	python3 manage.py load_county_data --input $< --table $@

etl/output/county_precincts_2020.geojson : etl/shapefiles/precincts/MS_VotingPrecincts_2020.shp
	ogr2ogr -f GeoJSON $@ $<

etl/shapefiles/precincts/%.shp : county_precincts_2020.zip
	unzip $< -d $(dir $@)

.INTERMEDIATE : county_precincts_2020.zip
county_precincts_2020.zip:
	curl -o $@ 'https://www.maris.state.ms.us/statewide/mstm/av/MS_VotingPrecincts_2020.zip'
