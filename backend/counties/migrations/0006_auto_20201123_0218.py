# Generated by Django 3.1.3 on 2020-11-23 02:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('counties', '0005_countygeojson'),
    ]

    operations = [
        migrations.AlterField(
            model_name='countygeojson',
            name='geojson',
            field=models.JSONField(),
        ),
    ]
