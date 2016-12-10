from django.db import models
from django.contrib.auth.models import User
from datetime import date

# Create your models here.

class tweetAnalysis(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    tweet = models.CharField(max_length=140)
    cleaned_tweet = models.CharField(max_length=140)
    text_character_count = models.IntegerField()
    textblob_senitment_polarity = models.DecimalField(max_digits=12, decimal_places=10)
    textblob_senitment_subjectivity = models.DecimalField(max_digits=8, decimal_places=7)
    flesch_kincaid = models.DecimalField(max_digits=6, decimal_places=3)
    coleman_liau_index = models.DecimalField(max_digits=6, decimal_places=3)
    flesch_reading_ease = models.DecimalField(max_digits=6, decimal_places=3)
    fog = models.DecimalField(max_digits=9, decimal_places=7)
    impact = models.CharField(max_length=50)
    # percent change is equal to scored labels that Azure returns
    percent_change = models.DecimalField(max_digits=30, decimal_places=28)
    date = models.DateField(default=date.today)
