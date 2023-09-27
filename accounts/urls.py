from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenBlacklistView,
)

from django.urls import path

from articles.views import ArticleListAPI, CommentAPI
from .views import FollowAPI, UserAPI

urlpatterns = [
    # 정보조회 / 회원가입 / 회원탈퇴
    path("user/", UserAPI.as_view(), name="user"),
    # 로그인
    path("api/token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("api/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    # 로그아웃
    path("api/token/blacklist/", TokenBlacklistView.as_view(), name="token_blacklist"),
    # 팔로우 기능 / 팔로우 조회
    path("<int:pk>/follow/", FollowAPI.as_view(), name="follow"),
    # 유저 게시글 조회
    path("<int:pk>/articles/", ArticleListAPI.as_view(), name="articles"),
    # 댓글 조회
    path("<int:pk>/comments/", CommentAPI.as_view(), name="comments"),
]
