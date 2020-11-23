from .models import County
from rest_framework import serializers

class CountySerializer(serializers.HyperlinkedModelSerializer):
	class Meta:
		model = County
		fields = ['fips', 'name']