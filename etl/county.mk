county_populations.csv: county_fips.csv
	curl -o $@ https://api.census.gov/data/2010/dec/sf1?get=group(P3)&for=county:001&in=state:28

county_fips.csv:
	curl -o $@ https://www2.census.gov/geo/docs/reference/codes/files/st28_ms_cou.txt

	cp $@ ../backend/counties/raw/$@