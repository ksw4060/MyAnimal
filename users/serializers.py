from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from rest_framework import serializers
from users.models import Users
from articles.serializers import ArticlesSerializer

from django.db.models.query_utils import Q

from django.conf import settings


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = Users
        exclude = ("followings",)

    def create(self, validated_data):
        user = super().create(validated_data)
        password = user.password
        user.set_password(password)
        user.save()
        return user

    def update(self, instance, validated_data):
        user = super().update(instance, validated_data)
        password = user.password
        user.set_password(password)
        user.save()
        return user


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['email'] = user.email
        token['account'] = user.account
        return token


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['email'] = user.email
        token['account'] = user.account
        return token


class UserProfileSerializer(serializers.ModelSerializer):
    followings = serializers.StringRelatedField(many=True)
    followers = serializers.StringRelatedField(many=True)
    hearts = serializers.StringRelatedField(many=True)
    bookmarks = serializers.StringRelatedField(many=True)
    # heartsed_articles = ArticlesSerializer(many=True, source="hearts"),
    # bookmarked_articles = ArticlesSerializer(many=True, source="bookmarks")

    class Meta:
        model = Users
        fields = ("id", "account", "followings", "followers",
                  "hearts", "bookmarks")
# 작성자 - 이준영
