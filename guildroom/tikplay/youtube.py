from guildroom.settings import YOUTUBE_API_KEY
import urllib.parse as urlparse
import requests
import json

def get_id_from_url(url):
    url_data = urlparse.urlparse(url)
    query = urlparse.parse_qs(url_data.query)
    if url_data.hostname == 'www.youtube.com' or url_data.hostname == 'youtube.com':
        try:
            video = query["v"][0]
        except:
            raise NoIdYoutubeUrlException("Could not find id field")
    elif url_data.hostname == 'www.youtu.be' or url_data.hostname == 'youtu.be':
        try:
            video = url_data.path.split('/')[1]
        except:
            raise NoIdYoutubeUrlException("Could not find id field")
    else:
        raise NotYoutubeUrlException('Not a youtube link')


    return video
        
class NotYoutubeUrlException(Exception):
    pass

class NoIdYoutubeUrlException(Exception):
    pass

