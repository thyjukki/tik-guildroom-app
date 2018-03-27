# tikplay/urls.py
from django.conf.urls import url
import sys
from tikplay import views
from queue import Queue

urlpatterns = [
    url(r'^$', views.add_song_view, name='index'),

    url(r'^api/queue/$', views.get_queue, name='api-queue'),
    url(r'^api/current/$', views.get_current, name='api-current'),
    url(r'^api/pop/$', views.pop_current, name='api-pop'),
    url(r'^api/add/$', views.add_song, name='api-add'),
    url(r'^api/play/$', views.play, name='api-play'),
    url(r'^api/toggleplay/$', views.toggleplay, name='api-toggleplay'),
    url(r'^api/is_paused/$', views.is_playing, name='api-is_playing'),
    url(r'^api/pause/$', views.pause, name='api-pause'),

    url(r'^api/log/$', views.get_history, name='api-log'),
]
