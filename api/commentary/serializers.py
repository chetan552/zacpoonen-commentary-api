from rest_framework import serializers
from .models import Commentary

class CommentarySerializer(serializers.ModelSerializer):
    class Meta:
        model = Commentary
        fields = '__all__'
