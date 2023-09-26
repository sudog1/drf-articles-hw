from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenBlacklistView,
)

from django.urls import path
from .views import UserView, articles_view, comments_view

urlpatterns = [
    path("user/", UserView.as_view(), name="user"),
    # login
    path("api/token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("api/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    # logout
    path("api/token/blacklist/", TokenBlacklistView.as_view(), name="token_blacklist"),

    path("articles/", articles_view, name="articles"),
    path("comments/", comments_view, name="comments"),
]
