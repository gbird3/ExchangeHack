from django.conf.urls import url

from . import views

app_name = 'smh2'
urlpatterns = [
    url(r'^index/$', views.index, name='index'),
    url(r'^tweet/$', views.tweet, name='tweet'),
    url(r'^tweets/$', views.all_tweets, name='tweets'),
    url(r'^results/$', views.results, name='results'),
    url(r'^dashboard/$', views.dashboard, name='dashboard'),
    url(r'^about/$', views.about, name='about'),
]
