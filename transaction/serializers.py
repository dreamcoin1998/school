from rest_framework import serializers
from .models import Commody, Type

class TypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Type
        fields = '__all__'


class CommodySerializer(serializers.ModelSerializer):
    class Meta:
        model = Commody
        fields = ('id', 'name', 'description', 'price', 'create_time', 'type', 'qq', 'wx', 'phone_number', 'yonghu', 'is_end', 'imagePath')
        depth = 2