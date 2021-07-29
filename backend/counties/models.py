from django.db import models
from django.urls import reverse

class County(models.Model):
	"""
	Represents a county in Mississippi. 
	Taken from the US Census 2010 FIPS Codes for Counties and County Equivalent Entities.
	https://www2.census.gov/geo/docs/reference/codes/files/st28_ms_cou.txt
	"""
	fips = models.CharField('FIPS Code', primary_key=True, max_length=3)
	name = models.CharField('County Name', max_length=50)
	state = models.CharField('State', max_length=2, default='MS')
	state_fips = models.CharField('State FIPS', max_length=2, default='28')
	fips_class = models.CharField('FIPS Class', max_length=2, default='H1')
	
	class Meta:
		ordering = ['fips']

	def __str__(self):
		return self.name

	def get_absolute_url(self):
		return reverse('county-detail', args=[str(self.fips)])


class Population(models.Model):
	county = models.ForeignKey(County, on_delete=models.CASCADE)
	year = models.IntegerField()
	survey = models.CharField(max_length=140)
	total = models.IntegerField()


class BaseGeoJSON(models.Model):
	"""
	Base model for storing GeoJSON.
	"""
	geojson = models.JSONField()

	class Meta:
		abstract = True


class CountyBorderGeoJSON(BaseGeoJSON):
	"""
	GeoJSON features that represent a county's border.
	"""
	county = models.ForeignKey(County, on_delete=models.CASCADE)

	def __str__(self):
		return self.county.name


class VotingPrecinct(BaseGeoJSON):
	"""
	A voting precinct within a county, aka "voting district".
	"""
	voting_district_code = models.CharField(max_length=20)
	county = models.ForeignKey(County, on_delete=models.CASCADE)
	name = models.CharField(max_length=140)
	name_area_description = models.CharField(max_length=280)
	# year
	# geojson_boundary

	def __str__(self):
		return f'{self.name} in {self.county.name}'


class VotingPrecinctGeoJSON(BaseGeoJSON):
	"""
	GeoJSON features that represent a VotingPrecinct's boundaries.
	"""
	precinct = models.ForeignKey(VotingPrecinct, on_delete=models.CASCADE)

	def __str__(self):
		return f'{self.precinct.name} in {self.precinct.county.name} County'
