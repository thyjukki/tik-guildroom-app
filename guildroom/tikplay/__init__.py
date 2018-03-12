# my_app/__init__.py
from queue import Queue
from tikplay.tikplayer import PlayerThread
default_app_config = 'tikplay.apps.tikplayConfig'

playerCommandQueue = Queue()
playerThread = PlayerThread(playerCommandQueue)
playerThread.daemon = True
playerThread.start()