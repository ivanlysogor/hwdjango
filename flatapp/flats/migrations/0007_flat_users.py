# Generated by Django 3.2 on 2021-07-06 13:12

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('flats', '0006_rename_synced_metervalues_mv_synced'),
    ]

    operations = [
        migrations.AddField(
            model_name='flat',
            name='users',
            field=models.ManyToManyField(to=settings.AUTH_USER_MODEL),
        ),
    ]