import json

from django.http import HttpResponse

def jsonp(func):
    def decorator(request, *args, **kwargs):
        objects = func(request, *args, **kwargs)
        callback = request.GET.get('callback', '')
            
        response = objects
        if callback:
            response = callback + '(' + response + ')'
        return HttpResponse(response, content_type="application/json")
    return decorator
