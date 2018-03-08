from django.shortcuts import render

from tikplay.forms import YoutubeForm
from tikplay.models import Song

import pafy
# Create your views here.
def add_song(request):
    if request.method == 'POST':
        form = YoutubeForm(request.POST)

        if form.is_valid():
            youtube_url = form.cleaned_data['youtube_url']
            video = pafy.new(youtube_url, basic=False)
            print (video.title)
            song = Song(url=youtube_url, title=video.title, audio_url=video.getbestaudio().url)
            song.save()
    else:
        form = YoutubeForm()

            
    return render(request, 'play_song.html', {'form': form})