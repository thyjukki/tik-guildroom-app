from rest_framework import serializers

from kiltacam.models import Camera

class SetCameraSerializer(serializers.ModelSerializer):
    class Meta:
        model = Camera
        fields = ('position', 'current')