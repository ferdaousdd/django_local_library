# Generated by Django 4.0.3 on 2023-05-19 10:53

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Auth', '0012_linestring_point_segment_linestring_points'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='segment',
            name='linestring',
        ),
        migrations.DeleteModel(
            name='LineString',
        ),
        migrations.DeleteModel(
            name='Point',
        ),
        migrations.DeleteModel(
            name='Segment',
        ),
    ]
