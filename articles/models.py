from django.db import models

from config.settings import AUTH_USER_MODEL

TOPIC_CHOICES = [
    ("all", "----"),
    ("game", "게임"),
    ("movie", "영화"),
    ("book", "책"),
    ("music", "음악"),
    ("picture", "그림"),
]


class Article(models.Model):
    author = models.ForeignKey(
        AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="articles"
    )
    title = models.CharField(max_length=128)
    content = models.TextField()
    topic = models.CharField(choices=TOPIC_CHOICES, max_length=64)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.title)


class Comment(models.Model):
    article = models.ForeignKey(
        Article, on_delete=models.CASCADE, related_name="comments"
    )
    author = models.ForeignKey(
        AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="comments"
    )
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
