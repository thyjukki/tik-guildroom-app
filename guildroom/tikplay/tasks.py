from multiprocessing import Process
from tikplay.models import Song
import subprocess

def get_audio_url(song_id):
    song = Song.objects.get(pk=song_id)
    url = "https://www.youtube.com/watch?v={}".format(song.video_id)
    output = subprocess.run(['youtube-dl', '--extract-audio', '--audio-quality','0', '-g' , url], stdout=subprocess.PIPE)
    song.audio_url = output.stdout.rstrip()
    song.save()
    

def pop():
    try:
        Song.objects.earliest().delete()
    except:
        return False

    return Song.objects.all().count() > 0