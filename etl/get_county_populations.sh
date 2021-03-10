#!/bin/bash

# get an array of fips from the input file
fips_array=($(awk -F, '{ print $3 }' $2))

python3 get_county_populations.py $2 $1

# counties=()
# header=$(curl "https://api.census.gov/data/2010/dec/sf1?get=group(P3)&for=county:001&in=state:28")
# #echo "${header[@]}," >> $1
# echo $header | jq '.[] .[]'

# for column in "${header[@]}"; do
# echo "column"
# 	echo $column
# done

# join () {
#   local IFS="$1"
#   shift
#   echo "$*"
# }

# string=$(join , "${header[@]}")
# echo $string




# # download the population data for each fips
# for fips in "${fips_array[@]}"; do
# 	county_pop=($(curl "https://api.census.gov/data/2010/dec/sf1?get=group(P3)&for=county:$fips&in=state:28" | jq .))
# 	echo "${county_pop[@]}"
# 	counties+="${county_pop[@]}"
# 	echo "${county_pop[*]}," >> $1
# done;




# querying a group
# https://api.census.gov/data/2010/dec/sf1?get=group(P3)&for=county:001&in=state:28
# https://www.census.gov/data/developers/updates/groups-functionality.html