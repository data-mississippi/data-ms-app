all : output/populations.json output/fips.csv output/county_borders_2020.geojson

include population.mk fips.mk borders.mk

clean : 
	rm output/*
	rm -r tl_2020_28_county20.*
