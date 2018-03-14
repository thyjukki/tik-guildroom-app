from django.apps import AppConfig
from tikplay import playerCommandQueue
import sys


class tikplayConfig(AppConfig):
    name = 'tikplay'

    def ready(self):
        if not 'runserver' in sys.argv:
            return True
        from queue import Queue
        from tikplay.tikplayer import PlayerThread

        if not playerThread:
            playerThread = PlayerThread(playerCommandQueue)
            playerThread.daemon = True
            playerThread.start()