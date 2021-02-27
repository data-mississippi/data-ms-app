county_borders_2020.geojson: tl_2020_28_county20.shp
	ogr2ogr -f GeoJSON frontend/public/geojson/county_borders_2020.geojson tl_2020_28_county20.shp
	cp frontend/public/geojson/county_borders_2020.geojson backend/counties/raw/county_borders_2020.geojson

tl_2020_28_county20.shp: county_borders_2020.zip
	unzip $<
	touch $@

county_borders_2020.zip:
	curl -o $@ 'https://www2.census.gov/geo/tiger/TIGER2020PL/LAYER/COUNTY/2020/tl_2020_28_county20.zip'
