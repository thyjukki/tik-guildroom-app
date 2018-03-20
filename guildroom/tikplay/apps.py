from django.apps import AppConfig
import sys


class tikplayConfig(AppConfig):
    name = 'tikplay'

    def ready(self):
        server = request.META.get('wsgi.file_wrapper', None)
        if 'runserver' in sys.argv or server:
            from tikplay import tikPlayer
            tikPlayer.run()