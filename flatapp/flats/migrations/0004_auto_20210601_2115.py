# Generated by Django 3.2 on 2021-06-01 21:15

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('flats', '0003_auto_20210601_2036'),
    ]

    operations = [
        migrations.RenameField(
            model_name='provider',
            old_name='provider_type_id',
            new_name='providertype_id',
        ),
        migrations.RenameField(
            model_name='providertype',
            old_name='provider_type_name',
            new_name='providertype_name',
        ),
        migrations.RenameField(
            model_name='providertype',
            old_name='provider_type_params',
            new_name='providertype_params',
        ),
    ]