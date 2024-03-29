borders : etl/output/county_borders_2020.geojson
	python3 manage.py load_county_data --input $< --table $@

etl/output/county_borders_2020.geojson : etl/shapefiles/tl_2020_28_county20.shp
	ogr2ogr -f GeoJSON $@ $<

etl/shapefiles/%.shp : county_borders_2020.zip
	unzip $< -d $(dir $@)

.INTERMEDIATE : county_borders_2020.zip
county_borders_2020.zip:
	curl -o $@ 'https://www2.census.gov/geo/tiger/TIGER2020PL/LAYER/COUNTY/2020/tl_2020_28_county20.zip'
