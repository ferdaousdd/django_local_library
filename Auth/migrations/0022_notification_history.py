# Generated by Django 4.0.3 on 2023-05-22 14:01

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('Auth', '0021_waterlevel'),
    ]

    operations = [
        migrations.CreateModel(
            name='Notification',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('zone', models.CharField(max_length=255)),
                ('point', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Auth.point')),
            ],
        ),
        migrations.CreateModel(
            name='History',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateTimeField(default=django.utils.timezone.now)),
                ('point', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Auth.point')),
                ('segment', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Auth.segment')),
            ],
        ),
    ]
