from django.shortcuts import render
from django.db.models import Max

from tikplay.forms import YoutubeForm
from tikplay.models import Song
from tikplay.youtube import get_id_from_url, get_video
# Create your views here.
def add_song(request):

    if request.method == 'POST':
        form = YoutubeForm(request.POST)

        if form.is_valid():
            youtube_url = form.cleaned_data['youtube_url']
            video_id = get_id_from_url(youtube_url)
            video = get_video(video_id)

            print (video.title)

            try:
                latest = Song.objects.latest()
                position_count = latest.position+1
            except Song.DoesNotExist:
                position_count = 0



            song = Song(video_id=video.id,
                        title=video.title,
                        description=video.description,
                        channel=video.channel,
                        image=video.image,
                        position=(position_count))
            song.save()
    else:
        form = YoutubeForm()
         
    song_list = Song.objects.all()
    return render(request, 'add_song.html', {'form': form, 'song_list': song_list})