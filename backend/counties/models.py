from django.db import models
from django.db.models import JSONField

class County(models.Model):
	"""Represents a county in Mississippi. 
	Taken from the US Census 2010 FIPS Codes for Counties and County Equivalent Entities.
	https://www2.census.gov/geo/docs/reference/codes/files/st28_ms_cou.txt
	"""

	fips = models.CharField(primary_key=True, max_length=3)
	name = models.CharField(max_length=50)
	state = models.CharField(max_length=2, default='MS')
	state_fips = models.CharField(max_length=2, default='28')
	fips_class = models.CharField(max_length=2, default='H1')
	
	class Meta:
		ordering = ['fips']

	def __str__(self):
		return self.name

class CountyGeoJSON(models.Model):
	county = models.ForeignKey(County, on_delete=models.CASCADE)
	geojson = JSONField()

	def __str__(self):
		return self.county.name