from django.shortcuts import render
from django.core import serializers
from django.http import HttpResponse

from rest_framework.decorators import api_view

from tikplay.forms import YoutubeForm
from tikplay.models import Song
from tikplay.youtube import get_id_from_url, get_video
from tikplay.decorators import jsonp
from tikplay import playerCommandQueue

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

            if position_count == 0:
                playerCommandQueue.put("NEW")
    else:
        form = YoutubeForm()
         
    song_list = Song.objects.all()
    ip = get('https://api.ipify.org').text
    try:
        current_song = Song.objects.earliest()
    except:
        current_song = None
    return render(request, 'add_song.html', {'form': form, 'song_list': song_list, 'ip': ip})

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
        print("Delete: {}".format(Song.objects.earliest()))
        Song.objects.earliest().delete()
    except:
        return json.dumps(json.loads("[]"), indent=4)
    try:
        output = serializers.serialize('json', [Song.objects.earliest()])
        print("New: {}".format(Song.objects.earliest()))
        playerCommandQueue.put("NEW")
        return json.dumps(json.loads(output), indent=4)
    except:
        playerCommandQueue.put("CLEAR")
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
         
    if position_count == 0:
        playerCommandQueue.put("NEW")
    output = serializers.serialize('json', Song.objects.all())
    return json.dumps(json.loads(output), indent=4)

@api_view(['GET'])
@jsonp
def play(request):
    playerCommandQueue.put("PLAY")
    return json.dumps({"message": "OK"}, indent=4)

@api_view(['GET'])
@jsonp
def pause(request):
    playerCommandQueue.put("PAUSE")
    return json.dumps({"message": "OK"}, indent=4)
