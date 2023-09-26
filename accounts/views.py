from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.generics import get_object_or_404
from rest_framework import status
from .serializers import FollowListSerializer, UserCreateSerializer, UserInfoSerializer
from django.contrib.auth import get_user_model, authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from django.db.models import Prefetch
from drf_yasg.utils import swagger_auto_schema


class UserAPI(APIView):
    # 정보 조회
    def get(self, request, format=None):
        if not request.user.is_authenticated:
            return Response({"detail": "권한이 없습니다."}, status=status.HTTP_403_FORBIDDEN)
        serializer = UserInfoSerializer(request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)

    # 회원가입
    @swagger_auto_schema(request_body=UserCreateSerializer)
    def post(self, request, format=None):
        serializer = UserCreateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # 회원탈퇴
    def delete(self, request, format=None):
        if not request.user.is_authenticated:
            return Response({"detail": "권한이 없습니다."}, status=status.HTTP_403_FORBIDDEN)
        user = request.user
        password = request.data.get("password", "")
        auth_user = authenticate(username=user.username, password=password)
        if auth_user:
            if not request.data.get("refresh"):
                return Response(
                    {"refresh": "토큰이 필요합니다."},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            token = RefreshToken(request.data.get("refresh"))
            auth_user.delete()
            token.blacklist()
            return Response({"message": "회원 탈퇴 완료."}, status=status.HTTP_204_NO_CONTENT)
        else:
            return Response({"detail": "비밀번호 불일치."}, status=status.HTTP_403_FORBIDDEN)


class FollowAPI(APIView):
    permission_classes = [IsAuthenticated]

    # 유저의 팔로우 조회
    def get(self, request, pk, format=None):
        target = get_object_or_404(
            get_user_model().objects.prefetch_related(
                Prefetch(
                    "followers", queryset=get_user_model().objects.only("nickname")
                ),
                Prefetch(
                    "followees", queryset=get_user_model().objects.only("nickname")
                ),
            ),
            pk=pk,
        )
        user = request.user
        # 맞팔로우일 때만 조회 가능
        if target != user:
            if (target in user.followers.all()) and (user in target.followers.all()):
                pass
            else:
                return Response(
                    {"detail": "권한이 없습니다."}, status=status.HTTP_403_FORBIDDEN
                )
        serializer = FollowListSerializer(target)
        return Response(serializer.data, status=status.HTTP_200_OK)

    # 팔로우 하기 / 취소
    def post(self, request, pk, format=None):
        target = get_object_or_404(get_user_model(), pk=pk)
        user = request.user
        if target == user:
            return Response({"detail": "권한이 없습니다."}, status=status.HTTP_403_FORBIDDEN)
        if target in user.followers.all():
            user.followers.remove(target)
            return Response({"message": "unfollow!"}, status=status.HTTP_200_OK)
        else:
            user.followers.add(target)
            return Response({"message": "follow!"}, status=status.HTTP_200_OK)
