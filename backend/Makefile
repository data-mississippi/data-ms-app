all : county borders population

clean : 
	find etl/shapefiles/ -type f -not -name .gitkeep -delete && \
	find etl/output/ -type f -not -name .gitkeep -delete && \
	(rm *.zip || :)

include etl/county.mk etl/population.mk etl/borders.mk etl/precincts.mk
