from rest_framework import serializers
from .models import Post


class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ('title','content','created_time','is_deleted','read_nums','num_views')
        depth = 2


