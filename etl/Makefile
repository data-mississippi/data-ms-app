.PHONY: all clean

#county_populations: raw_county_populations.csv
# get the names of the headers and make one csv
# https://api.census.gov/data/2010/dec/sf1/groups/P3.json

county_populations.json: county_fips.csv
	python3 get_county_populations.py $< $@
	
county_fips.csv:
	curl -o $@ https://www2.census.gov/geo/docs/reference/codes/files/st28_ms_cou.txt

	cp $@ ../backend/counties/raw/$@