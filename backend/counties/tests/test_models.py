import json
from django.test import TestCase
from django.db.models import JSONField
from counties.models import County, BaseGeoJSON, CountyBorderGeoJSON

class CountyModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        County.objects.create(name='Lee', fips='081')

    def test_fips_is_primary_key(self):
        county = County.objects.get(pk='081')
        self.assertEqual(county.pk, county.fips)

    def test_fips_label(self):
        county = County.objects.get(pk='081')
        field_label = county._meta.get_field('fips').verbose_name
        self.assertEqual(field_label, 'fips')

    def test_name_label(self):
        county = County.objects.get(pk='081')
        field_label = county._meta.get_field('name').verbose_name
        self.assertEqual(field_label, 'name')

    def test_fips_max_length(self):
        county = County.objects.get(pk='081')
        max_length = county._meta.get_field('fips').max_length
        self.assertEqual(max_length, 3)
    
    def test_name_max_length(self):
        county = County.objects.get(pk='081')
        max_length = county._meta.get_field('name').max_length
        self.assertEqual(max_length, 50)

    def test_state_is_mississippi(self):
        county = County.objects.get(pk='081')
        self.assertEqual(county.state, 'MS')

    def test_get_absolute_url(self):
        county = County.objects.get(pk='081')
        self.assertEqual(county.get_absolute_url(), '/counties/081/')


class CountyBorderGeoJSONModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        c = County.objects.create(name='Lee', fips='081')
        data = {}

        with open('counties/tests/lee-county-border.geojson') as json_file:
	        data = json.load(json_file)

        lee_county = CountyBorderGeoJSON(county=c, geojson=data)
        lee_county.save()

    def test_field_is_json(self):
        geojs = CountyBorderGeoJSON.objects.all()[0]
        field = geojs._meta.get_field('geojson')
        self.assertTrue(isinstance(field, JSONField))

    def test_belongs_to_county(self):
        county_fips = '081'
        geojs = CountyBorderGeoJSON.objects.filter(county__pk=county_fips)
        self.assertEqual(geojs[0].county.name, 'Lee')
        self.assertEqual(geojs[0].county.fips, county_fips)