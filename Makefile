all : etl/output/populations.json backend/counties/raw/fips.csv frontend/public/geojson/county_borders_2020.geojson

include etl/population.mk etl/fips.mk etl/borders.mk

clean : 
	rm etl/output/*
	rm backend/counties/raw/fips.csv
	rm frontend/public/geojson/county_borders_2020.geojson
	rm -r etl/tl_2020_28_county20.*
	rm -r tl_2020_28_county20.*
