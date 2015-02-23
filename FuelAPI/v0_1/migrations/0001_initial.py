# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='ApiKeys',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('api_key', models.CharField(max_length=15)),
                ('active', models.BooleanField(default=True)),
                ('validity', models.DateTimeField(default=datetime.datetime(2015, 3, 25, 18, 56, 42, 991600))),
                ('created_on', models.DateTimeField(default=datetime.datetime(2015, 2, 23, 18, 56, 42, 991625, tzinfo=utc), editable=False)),
                ('updated_on', models.DateTimeField(auto_now=True)),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='City',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=100, null=True, blank=True)),
                ('area', models.CharField(max_length=100, null=True, blank=True)),
                ('pincode', models.CharField(max_length=6, null=True, blank=True)),
                ('active', models.BooleanField(default=True)),
                ('latitude', models.TextField(null=True, blank=True)),
                ('longitude', models.TextField(null=True, blank=True)),
                ('created_on', models.DateTimeField(default=datetime.datetime(2015, 2, 23, 18, 56, 42, 989686, tzinfo=utc), editable=False)),
                ('updated_on', models.DateTimeField(auto_now=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Fuel',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=30, choices=[(b'petrol', b'Petrol'), (b'diesel', b'Diesel'), (b'cng', b'CNG'), (b'lpg', b'LPG')])),
                ('unit', models.CharField(max_length=9, choices=[(b'per kg', b'/KG'), (b'per litre', b'/L')])),
                ('active', models.BooleanField(default=True)),
                ('created_on', models.DateTimeField(default=datetime.datetime(2015, 2, 23, 18, 56, 42, 990137, tzinfo=utc), editable=False)),
                ('updated_on', models.DateTimeField(auto_now=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='FuelPrice',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('price', models.CharField(max_length=6)),
                ('active', models.BooleanField(default=True)),
                ('created_on', models.DateTimeField(default=datetime.datetime(2015, 2, 23, 18, 56, 42, 990683, tzinfo=utc), editable=False)),
                ('updated_on', models.DateTimeField(auto_now=True)),
                ('city', models.ForeignKey(to='v0_1.City')),
                ('fuel_type', models.ForeignKey(to='v0_1.Fuel')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Requests',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('url', models.URLField(help_text=b'the url that he requests')),
                ('ip', models.GenericIPAddressField(unpack_ipv4=True)),
                ('created_on', models.DateTimeField(default=datetime.datetime(2015, 2, 23, 18, 56, 42, 992084, tzinfo=utc), editable=False)),
                ('updated_on', models.DateTimeField(auto_now=True)),
                ('requester', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='State',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('short_name', models.CharField(max_length=10, null=True, blank=True)),
                ('long_name', models.CharField(max_length=50, null=True, blank=True)),
                ('active', models.BooleanField(default=True)),
                ('created_on', models.DateTimeField(default=datetime.datetime(2015, 2, 23, 18, 56, 42, 989190, tzinfo=utc), editable=False)),
                ('updated_on', models.DateTimeField(auto_now=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('contact_number', models.CharField(max_length=50, blank=True)),
                ('position', models.CharField(max_length=50, blank=True)),
                ('password_changed_on', models.DateTimeField(null=True, blank=True)),
                ('attempts', models.IntegerField(default=0)),
                ('last_attempt', models.DateTimeField(null=True, blank=True)),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL, unique=True)),
            ],
            options={
                'ordering': ('user__first_name', 'user__last_name'),
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='city',
            name='state',
            field=models.ForeignKey(to='v0_1.State'),
            preserve_default=True,
        ),
    ]
