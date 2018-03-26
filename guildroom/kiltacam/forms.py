from django import forms

from kiltacam.models import Camera

class SetImageForm(forms.ModelForm):
    current = forms.ImageField(required=True)

    class Meta:
        model = Camera
        fields = ('name', 'ip', 'position', 'current')
