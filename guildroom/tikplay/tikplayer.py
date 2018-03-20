
import json
import vlc
import youtube_dl
from tikplay.tasks import pop
from tikplay.models import Song
import threading


class Volume:
    def __int__(self, volume):
        self.volume = volume

class TiKPlayer ():
    def __init__(self):
        self.player = vlc.MediaPlayer()
        
        events = self.player.event_manager()
        events.event_attach(vlc.EventType.MediaPlayerEndReached, self.song_finished)
        self.playing = True
    def run(self):
        print ("Starting player")
        self.set_current_song()
        self.play()

    def set_current_song(self):
        print("set_current_song")
        try:
            song = Song.objects.earliest()
        except:
            return

        if not song:
            return

        self.player.set_media(vlc.Media(song.audio_url))

    def song_finished(self, event):
        print("Song finished")
        newSong = pop()
        if newSong:
            threading.Thread(target=self.new).start()
    
    def play(self):
        self.playing = True
        self.player.play()
    
    def new(self):
        print("New")
        self.stop()
        self.set_current_song()
        self.play()

    def pause(self):
        print("Pause")
        self.playing = False
        self.player.pause()

    def clear(self):
        print("Clear")
        self.stop()

    def stop(self):
        print("Stop")
        self.player.stop()

    def set_volume(self, volume):
        self.player.audio_set_volume(volume)

    def is_playing(self):
        return self.player.is_playing()

    
tikPlayer = TiKPlayer()