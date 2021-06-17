etl/output/populations.json:
	echo "populations"
	python3 etl/processors/get_county_populations.py > $@
