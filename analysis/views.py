from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django import forms
from django.contrib.auth.decorators import login_required
from datetime import datetime

from .models import tweetAnalysis

import re
from textblob import TextBlob
from nltk.corpus import stopwords

from .textstat import textstatistics
from .apostrophe import APPOSTROPHES
from .slang import SLANGS

from django.core.serializers.json import DjangoJSONEncoder
import urllib.request
import json

from decimal import *

# Create your views here.

@login_required(login_url='/account/login/')
def all_tweets(request):

	tweets = tweetAnalysis.objects.all().filter(user=request.user)

	template_vars = {
		'tweets': tweets
	}

	return render(request, 'analysis/tweets.html', template_vars)


@login_required(login_url='/account/login/')
def tweet(request):
	cached_stop_words = stopwords.words("english")
	form = TweetForm();

	if request.method == 'POST':
		form = TweetForm(request.POST)
		if form.is_valid():
			tweet = form.cleaned_data.get('tweet')
			## Start Text Cleaning
			text = tweet
			text = text.replace(',', '')
			text = text.replace('"', '')
			text = text.replace("''", '')
			if text.startswith('"') and text.endswith('"'):
				text = text[1:-1]

			# Apostrophe Lookup
			new_text_1 = []
			for word in text.split():
				word_lower = word.lower()
				if word_lower in APPOSTROPHES:
					new_text_1.append(APPOSTROPHES[word_lower])
				else:
					new_text_1.append(word)
			text_1 = " ".join(new_text_1)

			# Caching Stop-Words Part II
			new_text_2 = []
			for word in text_1.split():
				if word not in cached_stop_words:
					new_text_2.append(word)
			text_2 = " ".join(new_text_2)

			# Remove URLs
			new_text_3 = []
			for word in text_2.split():
				if not word.startswith("http") or word.startswith("www") or word.startswith("(h"):
					new_text_3.append(word)
			text_3 = " ".join(new_text_3)

			# Remove RT @name
			new_text_4 = []
			for word in text_3.split():
				word = re.sub('RT', '', word)
				word = re.sub('@\w+:', '', word)
				word = re.sub('@\w+', '', word)
				new_text_4.append(word)
			text_4 = " ".join(new_text_4)

			# Slangs Lookup
			new_text_5 = []
			for word in text_4.split():
				word_lower = word.lower()
				if word_lower in SLANGS:
					new_text_5.append(SLANGS[word_lower])
				else:
					new_text_5.append(word)
			text_5 = " ".join(new_text_5)
			cleaned_tweet = text_5

			# Character Count
			text_character_count = 0
			for word in text_5.split():
				characters = len(word)
				text_character_count = text_character_count + characters


    	## Start TextBlob Sentiment Analysis
			textblob_hold_sentiment = TextBlob(text_5)
            # Polarity = how negative(-1.0), neutral(0), positive(1.0)
			textblob_senitment_polarity = textblob_hold_sentiment.sentiment.polarity
			# Subjectivity = very objective(0.0), very subjective(1.0)
			textblob_senitment_subjectivity = textblob_hold_sentiment.sentiment.subjectivity
        ## End TextBlob Sentiment Analysis

	        ## Start Readability Analytics
			if re.search('[a-zA-Z]', text_5):
				txtstats = textstatistics()
				# Returns Gunning Fog index score
                # 17: College Graduate, 16: College Senior, 15: College Junior, 14: College Sophomore,
                # 13: College Freshman, 12: Highschool Senior, 11: Highschool Junior, 10: Highschool Sophomore,
                # 9: Highschool Freshman, 8: Eighth Grade, 7: Seventh Grade, 6: Sixth Grade
				fog = txtstats.gunning_fog(tweet)
                # Returns grade level using Flesch-Kincaid Grade Forumla
				flesch_kincaid = txtstats.flesch_kincaid_grade(tweet)
                # Returns grade level using Coleman-Liau Formula
				coleman_liau_index = txtstats.coleman_liau_index(tweet)
                # Returns Flesch Reading Ease Score
                # 90-100 : Very Easy, 80-89 : Easy, 70-79 : Fairly Easy, 60-69 : Standard,
                # 50-59 : Fairly Difficult, 30-49 : Difficult, 0-29 : Very Confusing
				flesch_reading_ease = txtstats.flesch_reading_ease(tweet)
	        ## End Readability Analytics

		data =  {

		        "Inputs": {

		                "input1":
		                {
		                    "ColumnNames": ["Text Character Count", "Textblob Senitment Polarity", "Textblob Senitment Subjectivity", "Flesch Kincaid", "Coleman Liau Index", "Flesch Reading Ease", "Gunning Fog"],
		                    "Values": [ [ text_character_count, textblob_senitment_polarity, textblob_senitment_subjectivity, flesch_kincaid, coleman_liau_index, flesch_reading_ease, fog ] ]
		                },        },
		            "GlobalParameters": {
		}
		    }

		body = str.encode(json.dumps(data, cls=DjangoJSONEncoder))

		url = 'https://ussouthcentral.services.azureml.net/workspaces/2c91e5bc8168471f9677a900994c4caa/services/ba80be8f78b54de78be85f4c2c5fac3d/execute?api-version=2.0&details=true'
		api_key = '7sWOgvwFvMjQBHcfJu9FydMSG7HGoqAznHD3wNxgHu0nDRLCRtfSIv1CUL6BCmCzf1S4HZHjOoCqbU+hyjBx1w==' # Replace this with the API key for the web service
		headers = {'Content-Type':'application/json', 'Authorization':('Bearer '+ api_key)}

		req = urllib.request.Request(url, body, headers)

		try:
			response = urllib.request.urlopen(req)
			result = response.read().decode('utf-8')
			json_object = json.loads(result)
			scoredLabels = Decimal(json_object['Results']['output1']['value']['Values'][0][0])

			percent_change = scoredLabels * 100

			if(scoredLabels > 0):
				impact = 'positive'
			else:
				impact = 'negative'

			print(cleaned_tweet)
		except urllib.error.HTTPError as error:
			print("The request failed with status code: " + str(error.code))
			# Print the headers - they include the request ID and the timestamp, which are useful for debugging the failure
			print(error.info())
			print(json.loads(error.read().decode("utf8", 'ignore')))

		t = tweetAnalysis()
		t.user = request.user
		t.tweet = tweet
		t.cleaned_tweet = cleaned_tweet
		t.text_character_count = text_character_count
		t.textblob_senitment_polarity = textblob_senitment_polarity
		t.textblob_senitment_subjectivity = textblob_senitment_subjectivity
		t.flesch_kincaid = flesch_kincaid
		t.coleman_liau_index = coleman_liau_index
		t.flesch_reading_ease = flesch_reading_ease
		t.fog = fog
		t.impact = impact
		t.percent_change = percent_change
		t.date = datetime.today()
		t.save()

		template_vars = {
			'tweet': tweet,
			'characters': text_character_count,
			'sentiment_polarity': textblob_senitment_polarity,
			'sentiment_subjectivity': textblob_senitment_subjectivity,
			'reading': flesch_reading_ease,
			'grade_level': coleman_liau_index,
			'impact': impact,
			'scoredLabels': percent_change * 100, #To get value as %
			'scoredLabels': round(percent_change, 7),
		}
		print(template_vars)
		return render(request, 'analysis/results.html', template_vars)

	template_vars = {
		'form': form,
	}

	return render(request, 'analysis/tweet.html', template_vars)

class TweetForm(forms.Form):
	tweet = forms.CharField(label='Enter tweet text', required=True, max_length=140, widget=forms.Textarea)

@login_required(login_url='/account/login/')
def results(request):
    return render(request, "analysis/results.html")

@login_required(login_url='/account/login/')
def dashboard(request):
    return render(request, "analysis/dashboard.html")

def about(request):
    return render(request, "analysis/about.html")

def index(request):
    return render(request, "analysis/index.html")
