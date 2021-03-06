# Generated by Django 3.2 on 2021-06-01 20:33

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Flat',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('flat_name', models.CharField(max_length=128, unique=True)),
                ('flat_address', models.TextField()),
            ],
            options={
                'db_table': 'flats',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='Meter',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('meter_name', models.CharField(max_length=128)),
                ('meter_params', models.TextField(null=True)),
                ('flat_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='flats.flat')),
            ],
            options={
                'db_table': 'meters',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='ProviderType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('provider_type_name', models.CharField(max_length=128, unique=True)),
                ('provider_type_params', models.TextField(null=True)),
            ],
            options={
                'db_table': 'provider_types',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='Provider',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('provider_name', models.CharField(max_length=128, unique=True)),
                ('provider_params', models.TextField(null=True)),
                ('provider_type_id', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='flats.providertype')),
            ],
            options={
                'db_table': 'providers',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='MeterValues',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('mv_date', models.DateField(auto_now=True)),
                ('mv_v1', models.FloatField(blank=True, null=True)),
                ('mv_v2', models.FloatField(blank=True, null=True)),
                ('mv_v3', models.FloatField(blank=True, null=True)),
                ('meter_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='flats.meter')),
            ],
            options={
                'db_table': 'meter_values',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='MeterType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('metertype_name', models.CharField(max_length=128, unique=True)),
                ('meter_type_params', models.TextField(null=True)),
                ('provider_id', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='flats.provider')),
            ],
            options={
                'db_table': 'meter_types',
                'managed': True,
            },
        ),
        migrations.AddField(
            model_name='meter',
            name='metertype_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='flats.metertype'),
        ),
    ]
