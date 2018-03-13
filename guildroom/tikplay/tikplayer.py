import threading
import time
import urllib.parse as urlparse
import requests
import json
import vlc
import youtube_dl

HOSTADRESS = "http://localhost:8000"

class Volume:
    def __int__(self, volume):
        self.volume = volume

class PlayerThread (threading.Thread):
    def __init__(self, queue):
        threading.Thread.__init__(self)
        self.queue = queue
        self.player = vlc.MediaPlayer()
        
        events = self.player.event_manager()
        events.event_attach(vlc.EventType.MediaPlayerEndReached, self.song_finished)
        self.playing = True
    def run(self):
        time.sleep(5)
        print ("Starting player")
        self.set_current_song()
        self.play()
        while True:
            try:
                val = self.queue.get(timeout=2)
                self.parse_message(val)
                self.queue.task_done()
            except:
                pass
        print ("Ending player")
    
    def parse_message(self, val):
        print("Player: " + val)
        if type(val) is str:
            if val == "PLAY":
                self.play()
            if val == "PAUSE":
                self.pause()
            if val == "CLEAR":
                self.clear()
            if val == "NEW":
                self.set_current_song()
                if self.playing:
                    self.play()
        elif type(val) is Volume:
            self.set_volume(val.volume)

    def set_current_song(self):
        get_url = '{}/api/current'.format(HOSTADRESS)
        result = requests.get(get_url)
        data = result.json()

        if not data:
            return None

        url = "https://www.youtube.com/watch?v={}".format(data[0]["fields"]["video_id"])
        ydl_opts = {
            'format': 'bestaudio',
        }
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(url, download=False)
            audio_url = info_dict.get("url", None)

        self.player.set_media(vlc.Media(audio_url))

    def song_finished(self, event):
        print("Song finished")
        get_url = '{}/api/pop'.format(HOSTADRESS)
        result = requests.get(get_url)
    
    def play(self):
        self.playing = True
        self.player.play()

    def pause(self):
        self.playing = False
        self.player.pause()

    def clear(self):
        self.player.stop()

    def set_volume(self, volume):
        self.player.audio_set_volume(volume)

