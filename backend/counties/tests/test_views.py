from django.test import TestCase
from django.urls import reverse
from counties.models import County

def create_counties(num):
    for i in range(num):
            County.objects.create(
                fips=f'00{i}',
                name=f'county-{i}'
            )

class CountyListViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        create_counties(9)

    def test_view_url_exists_at_desired_location(self):
        response = self.client.get('/counties/')
        self.assertEqual(response.status_code, 200)

    def test_lists_all_authors(self):
        response = self.client.get('/counties/')
        self.assertTrue(len(response.json()) == 8)


class CountyDetailViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        create_counties(9)

    def test_view_url_exists_at_desired_location(self):
        response = self.client.get('/counties/001/')
        self.assertEqual(response.status_code, 200)

    def test_detail_returns_data(self):
        response = self.client.get('/counties/001/')
        data = response.json()
        self.assertEqual(data['fips'], '001')
        self.assertEqual(data['name'], 'county-1')

    def test_invalid_detail_route(self):
        response = self.client.get('/counties/111/')
        self.assertEqual(response.status_code, 404)

# test should return 404
# http://localhost:8000/counties/geojson/borders/080/

# test should return lee county
# http://localhost:8000/counties/geojson/borders/081/