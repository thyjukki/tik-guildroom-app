from django.shortcuts import render
from django.core import serializers
from django.http import HttpResponse

from rest_framework.decorators import api_view

from tikplay.forms import YoutubeForm
from tikplay.models import Song
from tikplay.youtube import get_id_from_url, get_video
from tikplay.decorators import jsonp

import json
# Create your views here.

@api_view(['POST', 'GET'])
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

@api_view(['GET'])
@jsonp
def get_queue(request):
    output = serializers.serialize('json', Song.objects.all())
    return json.dumps(json.loads(output), indent=4)

@api_view(['GET'])
@jsonp
def get_current(request):
    try:
        output = serializers.serialize('json', [Song.objects.earliest()])
        return json.dumps(json.loads(output), indent=4)
    except:
        return json.dumps(json.loads("[]"), indent=4)

@api_view(['GET'])
@jsonp
def pop_current(request):
    try:
        Song.objects.earliest().delete()
        output = serializers.serialize('json', [Song.objects.earliest()])
        return json.dumps(json.loads(output), indent=4)
    except:
        return json.dumps(json.loads("[]"), indent=4)