# tikplay/urls.py
from django.conf.urls import url
from kiltacam import views

urlpatterns = [
    url(r'^api/add$', views.api_add_camera, name='api-add-cam'),
    url(r'^api/list$', views.api_get_cameras, name='api-list-cam'),
    url(r'^api/set', views.api_set_camera, name='api-set-cam'),
    url(r'^api/get', views.api_get_camera, name='api-get-cam'),
]
