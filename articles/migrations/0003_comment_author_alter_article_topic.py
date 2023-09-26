# Generated by Django 4.2.5 on 2023-09-26 07:10

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('articles', '0002_article_author_article_topic_comment'),
    ]

    operations = [
        migrations.AddField(
            model_name='comment',
            name='author',
            field=models.ForeignKey(default=4, on_delete=django.db.models.deletion.CASCADE, related_name='comments', to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='article',
            name='topic',
            field=models.CharField(choices=[('all', '----'), ('game', '게임'), ('movie', '영화'), ('book', '책'), ('music', '음악'), ('picture', '그림')], max_length=64),
        ),
    ]