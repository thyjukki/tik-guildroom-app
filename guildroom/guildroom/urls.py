"""
Definition of urls for guildroom.
"""

from datetime import datetime
from django.conf.urls import url, include
from django.conf.urls.static import static
import django.contrib.auth.views
from django.conf import settings
from django.contrib import admin

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
    url(r'^cam/*', include('kiltacam.urls')),

    # Tikplay
    url(r'^', include('tikplay.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
