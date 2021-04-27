# Generated by Django 3.2 on 2021-04-27 21:09

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Flat',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=64, unique=True)),
                ('address', models.TextField()),
                ('electricity_t1', models.IntegerField()),
                ('hot_water', models.IntegerField()),
                ('cold_water', models.IntegerField()),
            ],
        ),
    ]
