from rest_framework import serializers
from .models import Post,PostType

class PostTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostType
        fields = '__all__'

class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ('title','content','created_time','is_deleted','read_nums','num_views')
        depth = 2


