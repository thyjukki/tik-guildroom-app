from django.shortcuts import render
import pafy
import vlc

from tikplay.forms import YoutubeForm

# Create your views here.
def add_song(request):
    if request.method == 'POST':
        form = YoutubeForm(request.POST)

        if form.is_valid():
            youtube_url = form.cleaned_data['youtube_url']
            video = pafy.new(youtube_url)
            audio_url = video.getbestaudio().url
            print (audio_url)
            player = vlc.MediaPlayer(audio_url)
            player.play()
    else:
        form = YoutubeForm()

            
    return render(request, 'play_song.html', {'form': form})