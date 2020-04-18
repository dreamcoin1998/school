from .models import ImagePath
from rest_framework import serializers


class ImagePathSerializer(serializers.ModelSerializer):
    class Meta:
        model = ImagePath
        fields = ('imgPath',)