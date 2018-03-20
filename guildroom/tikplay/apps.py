from django.apps import AppConfig
import sys


class tikplayConfig(AppConfig):
    name = 'tikplay'

    def ready(self):
        if 'runserver' in sys.argv:
            from tikplay import tikPlayer
            tikPlayer.run()