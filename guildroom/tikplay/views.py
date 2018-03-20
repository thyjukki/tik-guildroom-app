from django.shortcuts import render
from django.core import serializers
from django.http import HttpResponse, HttpResponseRedirect

from rest_framework.decorators import api_view

from tikplay.forms import YoutubeForm
from tikplay.models import Song
from tikplay.youtube import get_id_from_url, get_video
from tikplay.decorators import jsonp
from tikplay.tikplayer import tikPlayer
from tikplay.tasks import get_audio_url, pop

import json
from requests import get
# Create your views here.

@api_view(['POST', 'GET'])
def add_song_view(request):

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
            

            get_audio_url(song.id)
    
            if position_count == 0:
                tikPlayer.new()

            return HttpResponseRedirect('/')
    else:
        form = YoutubeForm()
         
    song_list = Song.objects.all()
    try:
        current_song = Song.objects.earliest()
    except:
        current_song = None
    return render(request, 'add_song.html', {'form': form, 'song_list': song_list, 'current_song': current_song, 'playing': tikPlayer.is_playing()})

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

    nextSong = pop()

    if nextSong:
        output = serializers.serialize('json', [Song.objects.earliest()])
        tikPlayer.new()
        return json.dumps(json.loads(output), indent=4)
    else:
        tikPlayer.clear()
        return json.dumps(json.loads("[]"), indent=4)


@api_view(['GET'])
@jsonp
def add_song(request):
    url = request.GET.get('url')
    video_id = request.GET.get('id')
    if url: 
        try:
            video_id = get_id_from_url(url)
        except Exception as e:
            return json.dumps({"error": str(e)}, indent=4)

    
    if not video_id:
        return json.dumps({"error": "Missing parameter"}, indent=4)
    
    
    try:
        video = get_video(video_id)
    except Exception as e:
        return json.dumps({"error": str(e)}, indent=4)

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

    get_audio_url(song.id)
    
    if position_count == 0:
        tikPlayer.new()
    output = serializers.serialize('json', [song])
    return json.dumps(json.loads(output), indent=4)

@api_view(['GET'])
@jsonp
def play(request):
    tikPlayer.play()
    return json.dumps({"message": "OK"}, indent=4)

@api_view(['GET'])
@jsonp
def pause(request):
    tikPlayer.pause()
    return json.dumps({"message": "OK"}, indent=4)


@api_view(['GET'])
@jsonp
def toggleplay(request):
    if tikPlayer.is_playing():
        tikPlayer.pause()
        return json.dumps({"message": "PAUSE"}, indent=4)
    else:
        tikPlayer.play()
        return json.dumps({"message": "PLAY"}, indent=4)

@api_view(['GET'])
@jsonp
def is_playing(request):
    if tikPlayer.is_playing():
        return json.dumps({"message": "PLAYING"}, indent=4)
    else:
        return json.dumps({"message": "PAUSED"}, indent=4)