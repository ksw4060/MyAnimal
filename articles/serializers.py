from rest_framework import serializers
from articles.models import Articles, Comments


# articles
class ArticlesSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField()

    def get_user(self, obj):
        return obj.user.email

    class Meta:
        model = Articles
        fields = '__all__'


# comments
class CommentsSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField()

    def get_user(self, obj):
        return obj.user.email

    class Meta:
        model = Comments
        exclude = ("article",)  # 게시글빼고 보여주기


# comments작성
class CommentsCreatSerializer(serializers.ModelSerializer):
    pass


#
