from rest_framework import serializers
from .models import Commody, Type

class TypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Type
        fields = '__all__'


class CommodySerializer(serializers.ModelSerializer):
    class Meta:
        model = Commody
        fields = '__all__'
        depth = 2