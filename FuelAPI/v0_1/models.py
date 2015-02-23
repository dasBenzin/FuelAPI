from django.db import models
from django.utils import timezone

from datetime import datetime, timedelta

# The first element in each tuple is the actual value to be set on the model
# and the second element is the human-readable name
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
    created_on = models.DateTimeField(editable=False, default=timezone.now())
    updated_on = models.DateTimeField(auto_now=True)


class City(models.Model):
    name = models.CharField(max_length=100, blank=True, null=True)
    area = models.CharField(max_length=100, blank=True, null=True)
    pincode = models.CharField(max_length=6, blank=True, null=True)
    active = models.BooleanField(default=True)
    latitude = models.TextField(blank=True, null=True)
    longitude = models.TextField(blank=True, null=True)
    state = models.ForeignKey('State')
    created_on = models.DateTimeField(editable=False, default=timezone.now())
    updated_on = models.DateTimeField(auto_now=True)

'''Populate city and states - (if no proper DB/data is found)
http://en.wikipedia.org/wiki/List_of_cities_and_towns_in_India_by_population
1000 Indian cities DB - http://pastebin.com/Vi2GZX6S
'''


class Fuel(models.Model):
    name = models.CharField(max_length=30, choices=FUEL_NAMES)
    unit = models.CharField(max_length=9, choices=FUEL_UNIT_CHOICES)
    active = models.BooleanField(default=True)
    created_on = models.DateTimeField(editable=False, default=timezone.now())
    updated_on = models.DateTimeField(auto_now=True)


# each time a new row is inserted into this table
# we will have to deactivate the last inserted row for that fuel
# use pre_save()

class FuelPrice(models.Model):
    fuel_type = models.ForeignKey('Fuel')
    price = models.CharField(max_length=6)
    city = models.ForeignKey('City')
    # if active is True implies latest price
    active = models.BooleanField(default=True)
    created_on = models.DateTimeField(editable=False, default=timezone.now())
    updated_on = models.DateTimeField(auto_now=True)


class UserProfile(models.Model):
    # on delete we just make the user in active
    user = models.ForeignKey('auth.User', unique=True,)
    contact_number = models.CharField(max_length=50, blank=True)
    position = models.CharField(max_length=50, blank=True)
    password_changed_on = models.DateTimeField(null=True, blank=True)
    attempts = models.IntegerField(default=0)
    last_attempt = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ('user__first_name', 'user__last_name')

    def __unicode__(self):
        return self.user.get_full_name() or self.user.username


class ApiKeys(models.Model):
    user = models.ForeignKey('auth.User')
    api_key = models.CharField(max_length=15)
    # this will denote if the key is valid
    active = models.BooleanField(default=True)
    validity = models.DateTimeField(default=datetime.now() + timedelta(days=30))
    created_on = models.DateTimeField(editable=False, default=timezone.now())
    # this will let us know when he requested for a new key
    updated_on = models.DateTimeField(auto_now=True)

    def deactivate_key(self):
        self.active = False


class Requests(models.Model):
    # make entry here for user.id, lookup based on API key
    requester = models.ForeignKey('auth.User')
    url = models.URLField(help_text='the url that he requests')
    ip = models.GenericIPAddressField(unpack_ipv4=True)
    created_on = models.DateTimeField(editable=False, default=timezone.now())
    updated_on = models.DateTimeField(auto_now=True)

# TODO : add help_text whereever applicable
# https://docs.djangoproject.com/en/1.7/ref/models/fields/
