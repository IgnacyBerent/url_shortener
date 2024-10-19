from rest_framework import serializers
from .models import Url

class OutputUrlSerializer(serializers.ModelSerializer):
    class Meta:
        model = Url
        fields = '__all__'

class InputUrlSerializer(serializers.Serializer):
    original_url = serializers.URLField(max_length=200)