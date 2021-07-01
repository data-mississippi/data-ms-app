population : etl/output/population.json
	python3 manage.py load_county_data --input $< --table $@

etl/output/population.json:
	python3 etl/processors/get_county_populations.py > $@
