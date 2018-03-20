"""
Definition of urls for guildroom.
"""

from datetime import datetime
from django.conf.urls import url, include
import django.contrib.auth.views
from django.contrib import admin

from tikplay import urls
import youtube_dl

# Uncomment the next lines to enable the admin:
# from django.conf.urls import include
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = [
    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),

    # Tikplay
    url(r'^', include('tikplay.urls')),
]
