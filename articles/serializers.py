from rest_framework import serializers
from .models import Article, TOPIC_CHOICES


class ArticleSerializer(serializers.ModelSerializer):
    topic = serializers.ChoiceField(choices=TOPIC_CHOICES)

    class Meta:
        model = Article
        fields = (
            "author",
            "title",
            "content",
            "topic",
        )


class CommentSerializer(serializers.ModelSerializer):
    pass
