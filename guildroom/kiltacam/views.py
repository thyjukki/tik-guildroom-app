from django.shortcuts import render
from django.core import serializers
from django.http import HttpResponse, HttpResponseRedirect
from django.utils.datastructures import MultiValueDictKeyError
from django.shortcuts import get_object_or_404

from django.core.files.storage import default_storage
from django.core.files.base import ContentFile

from rest_framework.decorators import api_view

from kiltacam.decorators import jsonp
from kiltacam.models import Camera

import json
# Create your views here.

@api_view(['GET'])
@jsonp
def api_add_camera(request):
    if not request.user.is_authenticated:
        return json.dumps({'error': 'Not allowed to acces'}, indent=4)
    if request.method == 'GET':
        try:
            i = request.GET['ip']
            p = request.GET['position']
            n = request.GET['name']
            a = request.GET['token']
        except MultiValueDictKeyError:
            return json.dumps({'error': 'Missing parameters'}, indent=4)


        camera = Camera(ip=i, position=p, name=n, token=a)

        camera.save()
        output = serializers.serialize('json', [camera])
        return json.dumps(json.loads(output), indent=4)

    return json.dumps({'error': 'use get'}, indent=4)

@api_view(['GET'])
@jsonp
def api_get_cameras(request):
    if request.method == 'GET':
        output = serializers.serialize('json', Camera.objects.all())
        return json.dumps(json.loads(output), indent=4)
    return json.dumps({'error': 'use get'}, indent=4)

@api_view(['POST'])
def api_set_camera(request):
    if request.method == 'POST':
        photo_file = request.FILES['current']
        client_ip = request.META['REMOTE_ADDR']
        p = request.POST['position']
        a = request.POST['token']
        camera = Camera.objects.get(position=p, ip=client_ip, token=a)
        camera.current.save(photo_file.name, photo_file)
        return HttpResponse("ok")
    
def api_get_camera(request):
    i = request.GET['id']
    camera = get_object_or_404(Camera, pk=i)
    image_data = camera.current.read()
    return HttpResponse(image_data, content_type="image/png")