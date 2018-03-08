from django.shortcuts import render

from tikplay.forms import YoutubeForm

# Create your views here.
def add_song(request):
    if request.method == 'post':
        form = YoutubeForm(request.POST)

        if form.is_valid():
            youtube_url = form.youtube_url
    else:
        form = YoutubeForm()

            
    return render(request, 'play_song.html', {'form': form})