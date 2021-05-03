from django.db import models


class Flat(models.Model):
    name = models.CharField(max_length=64, unique=True)
    address = models.TextField()
    electricity_t1 = models.IntegerField()
    hot_water = models.IntegerField()
    cold_water = models.IntegerField()

    def flat_count(self):
        return Flat.objects.count()
