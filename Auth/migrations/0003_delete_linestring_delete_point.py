# Generated by Django 4.0.3 on 2023-05-16 18:24

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Auth', '0002_alter_user_image'),
    ]

    operations = [
        migrations.DeleteModel(
            name='LineString',
        ),
        migrations.DeleteModel(
            name='Point',
        ),
    ]
