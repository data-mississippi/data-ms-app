.PHONY: all clean

clean_county_populations.json: raw_county_populations.json
	python3 get_county_populations.py $< $@

raw_county_populations.json: county_fips.csv
	python3 get_county_populations.py $< $@
	
county_fips.csv:
	curl -o $@ https://www2.census.gov/geo/docs/reference/codes/files/st28_ms_cou.txt

	cp $@ ../backend/counties/raw/$@