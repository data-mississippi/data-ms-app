from django.contrib import admin
from .models import County, CountyGeoJSON

admin.site.register(County)
admin.site.register(CountyGeoJSON)
