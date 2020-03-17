from rest_framework import serializers
from .models import Commody, ImagePath, Message

class CommodySerializer(serializers.ModelSerializer):
    class Meta:
        model = Commody
        fields = ('name', 'description', 'price', 'read_num', 'create_time', 'type', 'qq', 'wx', 'phone_number', 'replyNum', 'floorNum')


class ImagePathSerializer(serializers.ModelSerializer):
    class Meta:
        model = ImagePath
        fields = ('imgPath',)


class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = ('msg', 'create_time', 'is_reply', 'floor')