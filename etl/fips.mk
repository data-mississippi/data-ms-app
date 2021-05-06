output/fips.csv:
	curl -o $@ https://www2.census.gov/geo/docs/reference/codes/files/st28_ms_cou.txt

	cp $@ ../backend/counties/raw/county_fips.csv
