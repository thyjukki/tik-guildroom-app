# tikplay/urls.py
from django.conf.urls import url

from tikplay import views

urlpatterns = [
    url(r'^$', views.add_song, name='index'),
]
