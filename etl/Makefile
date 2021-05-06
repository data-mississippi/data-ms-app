all : output/populations.json ../backend/counties/raw/fips.csv ../frontend/public/geojson/county_borders_2020.geojson

include population.mk fips.mk borders.mk

clean : 
	rm output/*
	rm ../backend/counties/raw/fips.csv
	rm ../frontend/public/geojson/county_borders_2020.geojson
	rm -r tl_2020_28_county20.*
