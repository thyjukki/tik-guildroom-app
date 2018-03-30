from django.apps import AppConfig
import sys

WSGI = 'django.core.wsgi' in sys.modules


class tikplayConfig(AppConfig):
    name = 'tikplay'

    def ready(self):
        if 'runserver' in sys.argv or WSGI:
            from tikplay.tikplayer import tikPlayer
            tikPlayer.run()