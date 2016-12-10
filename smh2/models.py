import uuid
import datetime

from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from django.utils import timezone
from django.contrib.auth.models import AbstractUser
from django.contrib import admin

@python_2_unicode_compatible
class Stock(models.Model):
    uid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100)
    ticker = models.CharField(max_length=7)
    openprice = models.DecimalField(max_digits=14, decimal_places=10, null=True, blank=True)
    closeprice = models.DecimalField(max_digits=14, decimal_places=10, null=True, blank=True)
    adjcloseprice = models.DecimalField(max_digits=14, decimal_places=10, null=True, blank=True)

    def __str__(self):
        stock = name + ": " + ticker
        return self.stock

class Tweet(models.Model):
    uid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    lang = models.CharField(max_length=10)
    location = models.CharField(max_length=100)
    name = models.CharField(max_length=100)
    screen_name = models.CharField(max_length=100)
    text = models.CharField(max_length=1000)
    text_polarity = models.DecimalField(max_digits=12, decimal_places=10)
    text_subjectivity = models.DecimalField(max_digits=12, decimal_places=10)
    time_zone = models.CharField(max_length=100)
    user_followers = models.IntegerField
    user_is_following = models.IntegerField
    user_tweets = models.IntegerField
    user_total_likes = models.IntegerField
    verified = models.CharField(max_length=100)

    def __str__(self):
        basic_info = 'Screen Name: ' + screen_name + ', Location: ' + location + ', Tweet: ' + text + ', Tweet Polarity: ' + text_polarity + ', Tweet Subjectivity: ' + text_subjectivity
        return self.basic_info

class tenK(models.Model):
    uid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
