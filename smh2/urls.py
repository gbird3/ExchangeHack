from django.conf.urls import url

from . import views

app_name = 'smh2'
urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^startTrack/$', views.startTrack, name='startTrack'),
    url(r'^$', views.terms_conditions, name='terms and conditions'),
    url(r'^$', views.privacy_policy, name='privacy policy'),
]
