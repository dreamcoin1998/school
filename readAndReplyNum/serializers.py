from rest_framework import serializers
from .models import ReadAndReplyNum


class ReadAndReplyNumSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReadAndReplyNum
        fields = ('read_num', 'reply_num')

    def save(self, **kwargs):
        super().save()