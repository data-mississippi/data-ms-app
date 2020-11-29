from django.contrib import admin
from .models import County, CountyBorderGeoJSON

admin.site.register(County)
admin.site.register(CountyBorderGeoJSON)
