from multiprocessing import Process
from tikplay import tikPlayer
from tikplay.models import Song
import youtube_dl

def get_audio_url(song_id, startSong):
    song = Song.objects.get(pk=song_id)
    url = "https://www.youtube.com/watch?v={}".format(song.video_id)
    ydl_opts = {
        'format': 'bestaudio',
    }
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        info_dict = ydl.extract_info(url, download=False)
        song.audio_url = info_dict.get("url", None)
        song.save()
    
    if startSong:
        tikPlayer.new()

def pop():
    try:
        Song.objects.earliest().delete()
    except:
        return False

    return Song.objects.all().count() == 1