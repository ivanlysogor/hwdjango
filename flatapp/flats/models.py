from django.db import models


class Flat(models.Model):
    flat_name = models.CharField(max_length=128, unique=True)
    flat_address = models.TextField()

    class Meta:
        managed = True
        db_table = 'flats'

    def flat_count(self):
        return Flat.objects.count()

    def __str__(self):
        return self.flat_name


class Provider(models.Model):
    provider_name = models.CharField(max_length=128, unique=True)

    def __str__(self):
        return self.provider_name


class MeterType(models.Model):
    metertype_name = models.CharField(max_length=128, unique=True)
    provider_id = models.ForeignKey(Provider, on_delete=models.CASCADE,
                                    null=True)

    def __str__(self):
        return self.metertype_name

    class Meta:
        managed = True
        db_table = 'meter_types'


class Meter(models.Model):
    meter_name = models.CharField(max_length=128)
    flat_id = models.ForeignKey(Flat, on_delete=models.CASCADE)
    metertype_id = models.ForeignKey(MeterType, on_delete=models.CASCADE)

    class Meta:
        managed = True
        db_table = 'meters'


class MeterValues(models.Model):
    meter_id = models.ForeignKey(Meter, on_delete=models.CASCADE)
    mv_date = models.DateField(auto_now=True)
    mv_v1 = models.FloatField(blank=True, null=True)
    mv_v2 = models.FloatField(blank=True, null=True)
    mv_v3 = models.FloatField(blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'meter_values'
