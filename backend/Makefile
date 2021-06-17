all : etl/output/population.json etl/output/fips.csv etl/output/county_borders_2020.geojson

clean : 
	find etl/shapefiles/ -type f -not -name .gitkeep -delete && \
	find etl/output/ -type f -not -name .gitkeep -delete && \
	(rm *.zip || :)

include etl/population.mk etl/fips.mk etl/borders.mk
