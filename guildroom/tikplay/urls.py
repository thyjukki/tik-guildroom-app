# tikplay/urls.py
from django.conf.urls import url

from tikplay import views

urlpatterns = [
    url(r'^$', views.add_song_view, name='index'),

    url(r'^api/queue/$', views.get_queue, name='api-queue'),
    url(r'^api/current/$', views.get_current, name='api-current'),
    url(r'^api/pop/$', views.pop_current, name='api-pop'),
    url(r'^api/add/$', views.add_song, name='api-add'),
]
