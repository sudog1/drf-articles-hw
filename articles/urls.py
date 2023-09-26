from django.urls import path
from .views import ArticleDetailAPI, ArticleListAPI, CommentAPI, LikeAPI

urlpatterns = [
    # 모든 게시글 조회 / 게시글 생성
    path("", ArticleListAPI.as_view(), name="articles_all"),
    # 유저 게시글 조회
    path("<int:pk>/", ArticleListAPI.as_view(), name="articles_user"),
    # 게시글 상세 / 수정 / 삭제 or 댓글 생성
    path(
        "<int:author_pk>/<int:article_pk>/", ArticleDetailAPI.as_view(), name="article"
    ),
    # 댓글 수정 / 삭제
    path(
        "<int:author_pk>/<int:article_pk>/<int:comment_pk>/",
        CommentAPI.as_view(),
        name="comments",
    ),
    # 좋아요 기능
    path("<int:author_pk>/<int:article_pk>/likes/", LikeAPI.as_view(), name="likes"),
]
