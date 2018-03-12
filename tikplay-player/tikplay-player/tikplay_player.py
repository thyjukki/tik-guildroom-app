import urllib.parse as urlparse
import requests
import json
import vlc
import pafy

HOSTADRESS = "http://localhost:8000"
def get_current_song_url():
        get_url = '{}/api/current'.format(HOSTADRESS)
        result = requests.get(get_url)
        data = result.json()

        if not data:
            return None

        url = "https://www.youtube.com/watch?v={}".format(data[0]["fields"]["video_id"])
        video = pafy.new(url)
        
        print(video.title)

        return video.getbestaudio().url

audio_url = get_current_song_url();

player = vlc.MediaPlayer(audio_url)
player.play()