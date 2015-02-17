from django.db import models
from datetime import datetime, timedelta

FUEL_NAMES = (
    ('petrol', 'Petrol'),
    ('diesel', 'Diesel'),
    ('cng', 'CNG'),
    ('lpg', 'LPG'),
)

FUEL_UNIT_CHOICES = (
    ('per kg', '/KG'),
    ('per litre', '/L'),
)


# Create your models here.
class State(models.Model):
    short_name = models.CharField(max_length=10, blank=True, null=True)
    long_name = models.CharField(max_length=50, blank=True, null=True)
    active = models.BooleanField(default=True)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)


class City(models.Model):
    name = models.CharField(max_length=100, blank=True, null=True)
    pincode = models.CharField(max_length=6, blank=True, null=True)
    active = models.BooleanField(default=True)
    latitude = models.TextField()
    longitude = models.TextField()
    state = models.ForeignKey('State')
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

'''Populate city and states - (if no proper DB/data is found) http://en.wikipedia.org/wiki/List_of_cities_and_towns_in_India_by_population
1000 Indian cities DB - http://pastebin.com/Vi2GZX6S
'''


class Fuel(models.Model):
    name = models.CharField(max_length=30, choices=FUEL_NAMES)
    unit = models.CharField(max_length=9, choices=FUEL_UNIT_CHOICES)
    active = models.BooleanField(default=True)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)


# each time a new row is inserted into this table, we will have to deactivate the last inserted row for that fuel
# use pre_save()

class FuelPrice(models.Model):
    fuel_type = models.ForeignKey('Fuel')
    price = models.CharField(max_length=6)
    city = models.ForeignKey('City')
    active = models.BooleanField(default=True)  # if active is True implies latest price
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)


class ApiKeys(models.Model):
    user = models.ForeignKey('auth.User')
    api_key = models.CharField(length=15)
    active = models.BooleanField(default=True)  # this will denote if the key is valid
    validity = models.DateTimeField(default=datetime.now() + timedelta(year=1))
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

# userprofile - stores info about users signing up for our API
# (django.contrib.auth) plus this profile


class Requests(models.Model):
    requester = models.ForeignKey('auth.User')  # make entry here for user.id, lookup based on API key
    url = models.TextField(help_text='the url that he requests')
    ip = models.CharField(length=12)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
