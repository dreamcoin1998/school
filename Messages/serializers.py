from rest_framework import serializers
from .models import MainMessage, ReplyMessage


class MainMessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = MainMessage
        fields = '__all__'
        depth = 2




class ReplyMessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReplyMessage
        fields = '__all__'
        depth = 2