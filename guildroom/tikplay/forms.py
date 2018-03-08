from django import forms

class YoutubeForm(forms.Form):
    youtube_url = forms.URLField(label='Youtube url')