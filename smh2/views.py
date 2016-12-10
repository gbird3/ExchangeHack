from django.conf import settings
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render
from django.urls import reverse
from django.views import generic
from django import forms
from textblob import TextBlob

import json
import argparse
import json
import sys
import re
import sys
import httplib2

## Import Database Tables
from django.contrib.auth.models import User
from .models import Stock, Tweet

#Google Service
def get_service():
    client = Client.from_service_account_json('/static/smh2/echangehack1-1504793b8e5e.json')
    credentials = GoogleCredentials.get_application_default()
    scoped_credentials = credentials.create_scoped(
        ['https://www.googleapis.com/auth/cloud-platform'])
    http = httplib2.Http()
    scoped_credentials.authorize(http)
    return discovery.build('language', 'v1beta1', http=http)

#Google entiment analysis
def get_googleSentiment(text):
    body = {
        'document': {
            'type': 'PLAIN_TEXT',
            'content': text,
        }
    }

    service = get_service()
    request = service.documents.analyzeSentiment(body=body)
    response = request.execute()

    return response

#Google entity analysis
def get_googleEntities(text):
    body = {
        'document': {
            'type': 'PLAIN_TEXT',
            'content': text,
        },
        "encodingType": "UTF8"
    }

    service = get_service()
    request = service.documents.analyzeEntities(body=body)
    response = request = execute()

    return response

def index(request):
    #try:
    #except .DoesNotExist:
        #raise Http404("Page does not exist")
    return render(request, "smh2/index.html")

def textblobSentimentAnalysis(text):
    sentiment = TextBlob(text)
    return sentiment

def startTrack(request):

    # config = {
    #     "apiKey": "AIzaSyCYaZJlTQjeI-SsWTzW6xplKc7Ja7I-s8Q",
    #     "authDomain": "exchangehack-143922.firebaseapp.com",
    #     "databaseURL": "https://exchangehack-143922.firebaseio.com/",
    #     "storageBucket": "exchangehack-143922.appspot.com",
    #     "serviceAccount": "/Users/pwill2/Desktop/HTN/smh/smh2/static/smh2/EHKEY.json"
    # }
    # firebase = pyrebase.initialize_app(config)
    # db = firebase.database()

    TRACK_TERMS = ['walmart', 'apple', 'google', 'gopro']
    #TRACK_TERMS = ['Walmart','Exxon Mobil','Apple','Berkshire Hathaway','McKesson','UnitedHealth Group','CVS Health','General Motors','Ford Motor','AT&T','General Electric','AmerisourceBergen','Verizon','Chevron','Costco','Fannie Mae','Kroger','Amazon.com','Amazon','Walgreens Boots Alliance','Walgreens','HP','Cardinal Health','Express Scripts Holding','J.P. Morgan Chase','Boeing','Microsoft','Bank of America Corp.','Wells Fargo','Home Depot','Citigroup','Phillips 66','IBM','Valero Energy','Anthem','Procter & Gamble','Alphabet','Comcast','Target','Johnson & Johnson','MetLife','Archer Daniels Midland','Marathon Petroleum','Freddie Mac','PepsiCo','United Technologies','Aetna',"Lowe’s",'UPS','AIG','Prudential Financial','Intel','Humana','Disney','Cisco Systems','Pfizer','Dow Chemical','Sysco','FedEx','Caterpillar','Lockheed Martin']
    CONSUMER_KEY = '0zvfK5MNq0dBg4Ymi1aZ3LgeJ'
    CONSUMER_SECRET = 'fXIYNVx5cjKR7dHz8QskYXCBQCNZR07Dsk0qf1TpnqXseVGN9m'
    ACCESS_TOKEN_KEY = '885756391-gy5jzaAGuIkSlVEMo38UTPAFIkYtUxPPDV6U5Xlt'
    ACCESS_TOKEN_SECRET = '1MAjzDlEipmz9NKq07JwJX8CXKoxmdwamBkn1wZvZVZZx'

    api = TwitterAPI(CONSUMER_KEY,
             CONSUMER_SECRET,
             ACCESS_TOKEN_KEY,
             ACCESS_TOKEN_SECRET)

    ##counter = db.child('counter').get().val()
    if counter is None:
        counter = 0
    r = api.request('statuses/filter', {'track': TRACK_TERMS})
    t = Tweet()
    for item in r.get_iterator():
        text = item['text']
        t.lang = item['user']['lang']
        t.location = item['user']['location']
        t.name = item['user']['name']
        t.screen_name =item['user']['screen_name']
        t.text = text
        t.time_zone =item['user']['time_zone']
        t.user_followers = item['user']['followers_count']
        t.user_is_following = item['user']['friends_count']
        t.user_tweets = item['user']['statuses_count']
        t.user_total_likes = item['user']['favourites_count']
        t.verified = item['user']['verified']

        #Sentiment Analysis -> TextBlob
        textblob_sentiment = textblobSentimentAnalysis(text)
        t.text_polarity = textblob_sentiment.sentiment.polarity
        t.text_subjectivity = textblob_sentiment.sentiment.subjectivity

        #Sentiment Analysis -> Google
        google_sentiment = get_googleSentiment(text)
        print(google_sentiment)

        #Entity Analysis -> Google
        google_entities = get_googleEntities(text)
        print(google_entities)

        print(t)
        if item['user']['lang'] == 'en':
            t.save()
        # data = {
        #     'lang': item['user']['lang'],
        #     'location': item['user']['location'],
        #     'name': item['user']['name'],
        #     'screen_name': item['user']['screen_name'],
        #     'text': item['text'],
        #     'time_zone': item['user']['time_zone'],
        #     'user_followers': item['user']['followers_count'],
        #     'user_is_following': item['user']['friends_count'],
        #     'user_tweets': item['user']['statuses_count'],
        #     'user_total_likes': item['user']['favourites_count'],
        #     'verified': item['user']['verified'],
        # }
        #The polarity score is a float within the range [-1.0, 1.0].
        #The subjectivity is a float within the range [0.0, 1.0]
            #0.0 is very objective
            #1.0 is very subjective


        #if data['lang'] == 'en':
            # db.child('tweets').push(data)
            # counter = counter + 1
            # db.child('counter').set(counter)

def terms_conditions(request):
    return HttpResponse("Terms and conditions page.")

def privacy_policy(request):
    return HttpResponse("Privacy policy page.")
