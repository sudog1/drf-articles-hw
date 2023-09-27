from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import get_user_model
from django.db.models import Count, Prefetch
from django.contrib.auth.hashers import make_password, check_password
from .models import Article, Comment
from .serializers import (
    ArticleCreateSerializer,
    ArticleDetailSerializer,
    ArticleListSerializer,
    CommentCreateSerializer,
    CommentListSerializer,
)
from drf_yasg.utils import swagger_auto_schema


class ArticleListAPI(APIView):
    # (전체 / 유저) 게시글 목록 조회
    def get(self, request, pk=None, format=None):
        if pk:
            articles = Article.objects.filter(author=pk)
        else:
            articles = Article.objects
        articles = (
            articles.select_related("author")
            .only("title", "topic", "author__nickname", "updated_at")
            .annotate(likes_count=Count("likes"), comments_count=Count("comments"))
        )
        serializer = ArticleListSerializer(articles, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    # 게시글 생성
    @swagger_auto_schema(request_body=ArticleCreateSerializer)
    def post(self, request, pk=None, format=None):
        if not request.user.is_authenticated:
            return Response({"detail": "권한이 없습니다."}, status=status.HTTP_403_FORBIDDEN)
        serializer = ArticleCreateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(author=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ArticleDetailAPI(APIView):
    # 게시글 상세 페이지
    def get(self, request, author_pk, article_pk, format=None):
        article = get_object_or_404(
            Article.objects.prefetch_related(
                Prefetch(
                    "comments__author",
                    queryset=get_user_model().objects.only("nickname"),
                ),
                Prefetch("likes", queryset=get_user_model().objects.only("nickname")),
            ),
            author=author_pk,
            pk=article_pk,
        )
        serializer = ArticleDetailSerializer(article)
        return Response(serializer.data, status=status.HTTP_200_OK)

    # (유저 / 익명 유저) 댓글 생성
    @swagger_auto_schema(request_body=CommentCreateSerializer)
    def post(self, request, author_pk, article_pk, format=None):
        article = get_object_or_404(Article, author=author_pk, pk=article_pk)
        password = request.data.pop("password", None)
        user = request.user if request.user.is_authenticated else None
        if user:
            pass
        elif password:
            password = make_password(password)
            pass
        else:
            return Response(
                {"detail": "로그인하거나 비밀번호를 입력하세요."}, status=status.HTTP_400_BAD_REQUEST
            )
        serializer = CommentCreateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(article=article, author=user, password=password)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # 게시글 수정
    @swagger_auto_schema(request_body=ArticleDetailSerializer)
    def put(self, request, author_pk, article_pk, format=None):
        article = get_object_or_404(Article, pk=article_pk, author=author_pk)
        if article.author != request.user:
            return Response({"detail": "권한이 없습니다."}, status=status.HTTP_403_FORBIDDEN)
        serializer = ArticleCreateSerializer(article, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # 게시글 삭제
    def delete(self, request, author_pk, article_pk, format=None):
        article = get_object_or_404(Article, pk=article_pk, author=author_pk)
        if article.author != request.user:
            return Response({"detail": "권한이 없습니다."}, status=status.HTTP_403_FORBIDDEN)
        article.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class CommentAPI(APIView):
    # 유저의 댓글 목록 조회
    def get(self, request, pk, format=None):
        if not request.user.is_authenticated:
            return Response({"detail": "권한이 없습니다."}, status=status.HTTP_403_FORBIDDEN)
        target = get_object_or_404(get_user_model(), pk=pk)
        user = request.user
        if target != user:
            if (target in user.followers.all()) and (user in target.followers.all()):
                pass
            else:
                return Response(
                    {"detail": "권한이 없습니다."}, status=status.HTTP_403_FORBIDDEN
                )
        serializer = CommentListSerializer(
            target.comments.select_related("author").only(
                "content", "author__nickname", "created_at"
            ),
            many=True,
        )
        return Response(serializer.data, status=status.HTTP_200_OK)

    # (유저 / 익명 유저) 댓글 수정
    @swagger_auto_schema(request_body=CommentCreateSerializer)
    def put(self, request, author_pk, article_pk, comment_pk, format=None):
        article = get_object_or_404(Article, pk=article_pk, author=author_pk)
        comment = get_object_or_404(Comment, pk=comment_pk)
        user = request.user if request.user.is_authenticated else None
        if comment.author:
            if comment.author != user:
                return Response(
                    {"detail": "권한이 없습니다."}, status=status.HTTP_403_FORBIDDEN
                )
        else:
            password = request.data.pop("password", None)
            if password:
                if check_password(password, comment.password):
                    pass
                else:
                    return Response(
                        {"detail": "잘못된 비밀번호입니다."},
                        status=status.HTTP_400_BAD_REQUEST,
                    )
            else:
                return Response(
                    {"detail": "로그인하거나 비밀번호를 입력하세요."},
                    status=status.HTTP_400_BAD_REQUEST,
                )
        serializer = CommentCreateSerializer(comment, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # (유저 / 익명 유저) 댓글 삭제
    def delete(self, request, author_pk, article_pk, comment_pk, format=None):
        article = get_object_or_404(Article, pk=article_pk, author=author_pk)
        comment = get_object_or_404(Comment, pk=comment_pk)
        user = request.user if request.user.is_authenticated else None
        # 게시글의 저자는 익명 댓글 삭제 가능
        if comment.author:
            if comment.author != user:
                return Response(
                    {"detail": "권한이 없습니다."}, status=status.HTTP_403_FORBIDDEN
                )
        else:
            if article.author == user:
                pass
            else:
                password = request.data.pop("password", None)
                if password:
                    if check_password(password, comment.password):
                        pass
                    else:
                        return Response(
                            {"detail": "잘못된 비밀번호입니다."},
                            status=status.HTTP_400_BAD_REQUEST,
                        )
                else:
                    return Response(
                        {"detail": "로그인하거나 비밀번호를 입력하세요."},
                        status=status.HTTP_400_BAD_REQUEST,
                    )
        comment.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class LikeAPI(APIView):
    permission_classes = [IsAuthenticated]

    # 좋아요 하기 / 취소
    def post(self, request, author_pk, article_pk, format=None):
        article = get_object_or_404(Article, pk=article_pk, author=author_pk)
        user = request.user
        if article.author == user:
            return Response({"detail": "권한이 없습니다."}, status=status.HTTP_403_FORBIDDEN)
        if article in user.likes.all():
            user.likes.remove(article)
            return Response({"message": "unlikes!"}, status=status.HTTP_200_OK)
        else:
            user.likes.add(article)
            return Response({"message": "likes!"}, status=status.HTTP_200_OK)
