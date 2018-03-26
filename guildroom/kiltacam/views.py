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
from kiltacam.forms import SetImageForm

import json
# Create your views here.

@api_view(['GET'])
@jsonp
def api_add_camera(request):
    if request.method == 'GET':
        try:
            i = request.GET['ip']
            p = request.GET['position']
            n = request.GET['name']
        except MultiValueDictKeyError:
            return json.dumps({'error': 'Missing parameters'}, indent=4)


        camera = Camera(ip=i, position=p, name=n)

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
        p = request.POST['position']
        camera = get_object_or_404(Camera, pk=p)

        photo_file.seek(0)
        path = default_storage.save(photo_file.name, ContentFile(photo_file.read()))
        camera.current.save(photo_file.name, photo_file)
        return HttpResponse("ok2")


def test_view(request):

    if request.method == 'POST':
        form = SetImageForm(request.POST, request.FILES)

        if form.is_valid():
            test = form.save()
            test.save()
    else:
        form = SetImageForm()
         
    return render(request, 'test.html', {'form': form})