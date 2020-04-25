from rest_framework import serializers
from .models import ReadAndReplyNum,LikeDetail,Likes


class ReadAndReplyNumSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReadAndReplyNum
        fields = ('read_num', 'reply_num')

    def save(self, **kwargs):
        super().save()

class LikesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Likes
        fields = ('like_num')

    def save(self, **kwargs):
        super().save()

class LikeDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = LikeDetail
        fields = ('created_time','is_liked')