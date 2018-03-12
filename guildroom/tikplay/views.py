from django.shortcuts import render
from django.db.models import Max

from tikplay.forms import YoutubeForm
from tikplay.models import Song
from guildroom.settings import YOUTUBE_API_KEY
import urllib.parse as urlparse
import requests
# Create your views here.
def add_song(request):

    if request.method == 'POST':
        form = YoutubeForm(request.POST)

        if form.is_valid():
            youtube_url = form.cleaned_data['youtube_url']

            url_data = urlparse.urlparse(youtube_url)
            query = urlparse.parse_qs(url_data.query)
            video = query["v"][0]

            get_url = 'https://www.googleapis.com/youtube/v3/videos?part=id%2C+snippet&id={}&key={}'.format(video, YOUTUBE_API_KEY)
            result = requests.get(get_url)
            print (result.json())

            position_count = song_list = Song.objects.all().aggregate(Max('rating'))



            song = Song.objects.get_or_create(url=youtube_url, defaults={ 'title': video.title, 'audio_url': video.getbestaudio().url, 'position': position_count})[0]
            song.save()
    else:
        form = YoutubeForm()
         
    song_list = Song.objects.all()
    return render(request, 'add_song.html', {'form': form, 'song_list': song_list})