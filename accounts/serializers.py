from rest_framework import serializers
from .models import User
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token["nickname"] = user.nickname
        return token


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = (
            "username",
            "email",
            "password",
            "fullname",
            "nickname",
        )

    normalized_fields = ["username", "email", "nickname"]

    def is_valid(self, *, raise_exception=False):
        for field in self.normalized_fields:
            if field == "email":
                self.initial_data["email"] = get_user_model().objects.normalize_email(
                    self.initial_data.get(field)
                )
            else:
                self.initial_data[field] = (
                    get_user_model()
                    .normalize_username(self.initial_data.get(field) or "")
                    .lower()
                )
        return super().is_valid(raise_exception=raise_exception)

    def create(self, validated_data):
        return get_user_model().objects.create_user(**validated_data)
    
    def update(self, validated_data):
        return get_user_model().objects.create_user(**validated_data)
