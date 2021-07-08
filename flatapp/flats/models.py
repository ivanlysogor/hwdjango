from django.db import models
from django.contrib.auth.models import User

class Flat(models.Model):
    flat_name = models.CharField(max_length=128, unique=True)
    flat_address = models.TextField(null=True)
    users = models.ManyToManyField(User)

    def flat_count(self):
        return Flat.objects.count()

    def __str__(self):
        return self.flat_name

    class Meta:
        managed = True
        db_table = 'flats'

class ProviderType(models.Model):
    providertype_name = models.CharField(max_length=128, unique=True)
    providertype_params = models.TextField(null=True, blank= True)

    def __str__(self):
        return self.providertype_name

    class Meta:
        managed = True
        db_table = 'provider_types'

class Provider(models.Model):
    provider_name = models.CharField(max_length=128, unique=True)
    providertype_id = models.ForeignKey(ProviderType, on_delete=models.CASCADE,
                                    null=True)
    provider_params = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.provider_name

    class Meta:
        managed = True
        db_table = 'providers'


class MeterType(models.Model):
    metertype_name = models.CharField(max_length=128, unique=True)
    provider_id = models.ForeignKey(Provider, on_delete=models.CASCADE,
                                    null=True)
    meter_type_params = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.metertype_name

    class Meta:
        managed = True
        db_table = 'meter_types'


class Meter(models.Model):
    meter_name = models.CharField(max_length=128)
    flat_id = models.ForeignKey(Flat, on_delete=models.CASCADE)
    metertype_id = models.ForeignKey(MeterType, on_delete=models.CASCADE)
    meter_params = models.TextField(null=True, blank=True)

    class Meta:
        managed = True
        db_table = 'meters'


class MeterValues(models.Model):
    meter_id = models.ForeignKey(Meter, on_delete=models.CASCADE)
    mv_date = models.DateTimeField(auto_now=True)
    mv_v1 = models.FloatField(blank=True, null=True)
    mv_v2 = models.FloatField(blank=True, null=True)
    mv_v3 = models.FloatField(blank=True, null=True)
    mv_synced = models.BooleanField(default=False)


    class Meta:
        managed = True
        db_table = 'meter_values'
