# tikplay/urls.py
from django.conf.urls import url
import sys
from tikplay import views
from queue import Queue
from tikplay.tikplayer import PlayerThread
from tikplay import playerCommandQueue

if 'runserver' in sys.argv:
    playerThread = PlayerThread(playerCommandQueue)
    playerThread.daemon = True
    playerThread.start()

urlpatterns = [
    url(r'^$', views.add_song_view, name='index'),

    url(r'^api/queue/$', views.get_queue, name='api-queue'),
    url(r'^api/current/$', views.get_current, name='api-current'),
    url(r'^api/pop/$', views.pop_current, name='api-pop'),
    url(r'^api/add/$', views.add_song, name='api-add'),
    url(r'^api/play/$', views.play, name='api-play'),
    url(r'^api/pause/$', views.pause, name='api-pause'),
]
