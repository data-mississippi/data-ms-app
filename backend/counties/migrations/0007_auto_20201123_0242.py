# Generated by Django 3.1.3 on 2020-11-23 02:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('counties', '0006_auto_20201123_0218'),
    ]

    operations = [
        migrations.AlterField(
            model_name='county',
            name='state_fips',
            field=models.CharField(default='28', max_length=2),
        ),
    ]
