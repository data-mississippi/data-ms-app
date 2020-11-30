from django.contrib import admin
from .models import County, CountyBorderGeoJSON, VotingPrecinct

admin.site.register(County)
admin.site.register(CountyBorderGeoJSON)
admin.site.register(VotingPrecinct)