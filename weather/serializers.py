from django.contrib.auth.models import User

from rest_framework import serializers
from weather.models import Weather


class WeatherSerializer(serializers.Serializer):
    city = serializers.CharField(
        max_length=256, allow_blank=False, allow_null=False)
    # date = serializers.DateField(allow_null=False)
    # time = serializers.TimeField(allow_null=False)
    currently_temperature = serializers.FloatField()
    daily_temperature_max = serializers.FloatField()
    daily_temperature_min = serializers.FloatField()
    weekly_temperature_max = serializers.FloatField()
    weekly_temperature_min = serializers.FloatField()

    def create(self, validated_data):
        """
        Create and return a new `Weather` instance, given the validated data.
        """
        return Weather.objects.create(**validated_data)


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'password']

