from rest_framework import serializers
from articles.models import Articles, Comments


class ArticlesSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField()

    def get_user(self, obj):
        return obj.user.nickname

    class Meta:
        model = Articles
        fields = "__all__"

   
class ArticlesCreateSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField()
    article_created_at = serializers.DateTimeField(
        format='%Y-%m-%d', read_only=True)
    article_updated_at = serializers.DateTimeField(
        format='%Y-%m-%d', read_only=True)

    def get_user(self, obj):
        return {'nickname': obj.user.nickname, 'pk': obj.user.pk}

    class Meta:
        model = Articles
        fields = ("pk", "user", "article_title", "article_content",
                  "article_img", "category", "article_created_at", "article_updated_at")


class ArticlesUpdateSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField()

    def get_user(self, obj):
        return {'nickname': obj.user.nickname, 'pk': obj.user.pk}

    class Meta:
        model = Articles
        fields = ("pk", "user", "article_title",
                  "article_content", "article_img", "category")

# comments


class CommentsSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField()
    comment_created_at = serializers.DateTimeField(
        format='%Y-%m-%d', read_only=True)
    comment_updated_at = serializers.DateTimeField(
        format='%Y-%m-%d', read_only=True)

    def get_user(self, obj):
        return {'nickname': obj.user.nickname, 'pk': obj.user.pk}

    class Meta:
        model = Comments
        exclude = ('article',)  # 게시글 필드 빼고 보여주기


# comments작성
class CommentsCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comments
        fields = ("comment",)


#
