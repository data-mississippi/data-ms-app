county : etl/output/fips.csv
	python3 manage.py load_county_data --input $< --table $@

etl/output/fips.csv:
	curl -o $@ https://www2.census.gov/geo/docs/reference/codes/files/st28_ms_cou.txt
