from rest_framework import serializers
from .models import Article, TOPIC_CHOICES, Comment


class ArticleListSerializer(serializers.ModelSerializer):
    author = serializers.SerializerMethodField()
    likes_count = serializers.IntegerField()
    comments_count = serializers.IntegerField()

    def get_author(self, obj):
        author = obj.author
        if author:
            return {"pk": author.pk, "nickname": author.nickname}
        else:
            return None

    class Meta:
        model = Article
        fields = (
            "pk",
            "title",
            "topic",
            "author",
            "likes_count",
            "comments_count",
            "updated_at",
        )


class CommentListSerializer(serializers.ModelSerializer):
    author = serializers.SerializerMethodField()

    def get_author(self, obj):
        author = obj.author
        if author:
            return {"pk": author.pk, "nickname": author.nickname}
        else:
            return None

    class Meta:
        model = Comment
        fields = (
            "pk",
            "content",
            "author",
            "created_at",
        )


class ArticleDetailSerializer(serializers.ModelSerializer):
    author = serializers.SerializerMethodField()
    comments = CommentListSerializer(many=True)
    comments_count = serializers.SerializerMethodField()
    likes = serializers.SerializerMethodField()

    def get_author(self, obj):
        author = obj.author
        if author:
            return {"pk": author.pk, "nickname": author.nickname}
        else:
            return None

    def get_likes(self, obj):
        return [{"pk": user.pk, "nickname": user.nickname} for user in obj.likes.all()]

    def get_comments_count(self, obj):
        return obj.comments.count()

    class Meta:
        model = Article
        fields = "__all__"


class ArticleCreateSerializer(serializers.ModelSerializer):
    topic = serializers.ChoiceField(choices=TOPIC_CHOICES)

    class Meta:
        model = Article
        fields = (
            "title",
            "content",
            "topic",
        )


class CommentCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ("content",)
