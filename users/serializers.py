from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from rest_framework import serializers
from users.models import Image, Users
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




# 빈 값을 넣으면 default 가 안된다.


class UserProfileSerializer(serializers.ModelSerializer):
    followings = serializers.StringRelatedField(many=True)
    followers = serializers.StringRelatedField(many=True)
    hearts = serializers.StringRelatedField(many=True)
    bookmarks = serializers.StringRelatedField(many=True)
    profile_img = serializers.ImageField(
        max_length=None,
        use_url=True,
        required=False,  # 입력값이 없어도 유효성 검사를 통과
        # allow_null=True,
        default=settings.DEFAULT_PROFILE_IMAGE
    )
    # heartsed_articles = ArticlesSerializer(many=True, source="hearts"),
    # bookmarked_articles = ArticlesSerializer(many=True, source="bookmarks")

    class Meta:
        model = Users
        fields = ("account", "nickname",
                  "email", "profile_img",
                  "category", "followings",
                  "followers", "hearts", "bookmarks")

    def clean_img(self):
        img = self.cleaned_data.get('profile_img')
        if img and img.size > 2 * 1024 * 1024:  # 2mb
            raise serializers.ValidationError('이미지 크기는 최대 2mb까지 가능해요.')
        return img
# 작성자 - 이준영


class ImageSerializer(serializers.ModelSerializer):
    image = serializers.ImageField(max_length=None, use_url=True)

    class Meta:
        model = Image
        fields = ('id', 'image')
# 작성자 - 이준영
