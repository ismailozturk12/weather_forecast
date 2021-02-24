import requests
import datetime

from django.http import HttpResponse, JsonResponse
from django.core.cache import cache
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt

from rest_framework.parsers import JSONParser
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework import viewsets
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated

from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema

from weather.serializers import WeatherSerializer, UserSerializer
from weather.models import Weather


def fahrenheit_to_celsius(value):
    return round(((value - 32) * 5.0/9.0), 2)

def cache_key_generate(city):
    date = date.today()
    return '{}_{}'.format(city, date)

def get_location(city):
    get_location_url = 'https://eu1.locationiq.com/v1/search.php?key=a1779b7817b3b2&q=[{}]&format=json'.format(
        city)
    
    req = requests.post(get_location_url)
    location = req.json()
    lat = location[0].get('lat')
    lon = location[0].get('lon')

    return lat, lon

def get_temperature_data(lat, lon):
    get_data_url = 'https://api.darksky.net/forecast/f3146e0fc78b4930d41a60703c08e2ae/{lat},{lon}'.format(
        lat=lat, lon=lon)
    
    req = requests.get(get_data_url)
    temperature = req.json()

    return temperature


city_param = openapi.Parameter(
    'city', openapi.IN_QUERY, description="city", type=openapi.TYPE_STRING)


@csrf_exempt
@swagger_auto_schema(method='post', manual_parameters=[city_param])
@api_view(['POST'])
@authentication_classes([SessionAuthentication, BasicAuthentication])
@permission_classes([IsAuthenticated])
def weaters(request):
    """
    Weather Forecast
    """
    date = datetime.date.today()
    city = request.GET.get('city')
    cache_key_generate = '{}_{}'.format(city, date)
    cache_data = cache.get(cache_key_generate)
    if cache_data:
        return JsonResponse(cache_data)
    weater = Weather.objects.filter(city=city, date=date).first()
    if not weater:
        lat, lon = get_location(city)
        temperature = get_temperature_data(lat,lon)
        currently_temperature = temperature['currently']['temperature']
        currently_temperature_celsius = fahrenheit_to_celsius(
            currently_temperature)
        daily_data = temperature.get('daily')['data']
        daily_temperature_max = daily_data[0]['temperatureMax']
        daily_temperature_min = daily_data[0]['temperatureLow']
        weekly_temperature_max = 0
        weekly_temperature_min = 0
        for daily in daily_data:
            if weekly_temperature_max < daily.get('temperatureMax'):
                weekly_temperature_max = daily.get('temperatureMax')
            if weekly_temperature_min < daily.get('temperatureMin'):
                weekly_temperature_min = daily.get('temperatureMin')
        
        response = {
            'city': city,
            'currently_temperature': currently_temperature_celsius,
            'daily_temperature_max': fahrenheit_to_celsius(daily_temperature_max),
            'daily_temperature_min': fahrenheit_to_celsius(daily_temperature_min),
            'weekly_temperature_max': fahrenheit_to_celsius(weekly_temperature_max),
            'weekly_temperature_min': fahrenheit_to_celsius(weekly_temperature_min)
        }

        serializer = WeatherSerializer(data=response)
        if serializer.is_valid(raise_exception=False):
            serializer.save()
            cache.set(cache_key_generate, serializer.data)
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)

    serializer = WeatherSerializer(weater)
    cache.set(cache_key_generate, serializer.data)
    return JsonResponse(serializer.data)


class UserViewSet(viewsets.ModelViewSet):
    """
    A viewset for viewing and editing user instances.
    """
    serializer_class = UserSerializer
    queryset = User.objects.all()

    def perform_create(self, serializer):
        instance = serializer.save()
        instance.set_password(instance.password)
        instance.save()
