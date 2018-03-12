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

def get_video(id):
    return Video(id)


class Video:
    def __init__(self, video_id):
        self.id = video_id
        
        get_url = 'https://www.googleapis.com/youtube/v3/videos?part=id%2C+snippet&id={}&key={}'.format(self.id, YOUTUBE_API_KEY)
        result = requests.get(get_url)
        data = result.json()

        results = data['pageInfo']['totalResults']

        if results != 1:
            raise NoVideoYoutubeException('No video found by id')
        
        item = data['items'][0]['snippet']
        self.title = item['title']
        self.description = item['description']
        self.channel = item['channelTitle']
        self.image = item['thumbnails']['maxres']['url']
        
class NotYoutubeUrlException(Exception):
    pass

class NoIdYoutubeUrlException(Exception):
    pass

class NoVideoYoutubeException(Exception):
    pass

