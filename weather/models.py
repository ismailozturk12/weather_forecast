from django.db import models

class Weather(models.Model):
    city = models.CharField(
        max_length=256
    )
    date = models.DateField(
        auto_now=True
    )
    time = models.TimeField(
        auto_now=True
    )
    currently_temperature = models.FloatField()
    daily_temperature_max = models.FloatField()
    daily_temperature_min = models.FloatField()
    weekly_temperature_max = models.FloatField()
    weekly_temperature_min = models.FloatField()
