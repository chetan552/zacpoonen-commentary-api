from rest_framework import serializers
from .models import Commentary

class CommentarySerializer(serializers.ModelSerializer):
    class Meta:
        model = Commentary
        fields = '__all__'

class CommentarySearchSerializer(serializers.ModelSerializer):
    snippet = serializers.SerializerMethodField()

    class Meta:
        model = Commentary
        fields = ['id', 'book', 'chapter', 'verse', 'snippet']

    def get_snippet(self, obj):
        terms = self.context.get('terms') or []
        text = obj.text or ''
        lowered = text.lower()

        # Find first occurrence of any term (case-insensitive)
        hit_index = None
        for term in terms:
            idx = lowered.find(term.lower())
            if idx != -1:
                hit_index = idx
                break

        snippet_length = 200
        if hit_index is None:
            start = 0
        else:
            start = max(hit_index - snippet_length // 4, 0)

        end = min(start + snippet_length, len(text))
        snippet = text[start:end].strip()

        prefix = '...' if start > 0 else ''
        suffix = '...' if end < len(text) else ''
        return f"{prefix}{snippet}{suffix}"
