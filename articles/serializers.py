from rest_framework import serializers
from articles.models import Articles, Comments

# 이미지 업로드 시리얼라이저 - 이미지 직렬화
# class ArticleImageSerializer(serializers.ModelSerializer):
#     image = serializers.ImageField(use_url=True)

#     class Meta:
#         model = ArticleImage
#         fields = ['image']


class ArticlesSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField()

    def get_user(self, obj):
        return obj.user.nickname

    class Meta:
        model = Articles
        fields = "__all__"

    # #게시글에 등록된 이미지들 가지고 오기
    # def get_images(self, obj):
    #     image = obj.image.all()
    #     return ArticleImageSerializer(instance=image, many=True, context=self.context).data

    # def create(self, validated_data):
    #     instance = Articles.objects.create(**validated_data)
    #     image_set = self.context['request'].FILES
    #     for image_data in image_set.getlist('image'):
    #         ArticleImage.objects.create(article=instance, image=image_data)
    #     return instance


class ArticlesCreateSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField()
    
    def get_user(self, obj):
        return obj.user.nickname
    class Meta:
        model = Articles
        fields = ("pk", "user","article_title", "article_content",
                  "article_img", "category","article_created_at","article_updated_at")


class ArticlesUpdateSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField()

    def get_user(self, obj):
        return obj.user.nickname

    class Meta:
        model = Articles
        fields = ("pk", "user", "article_title",
                  "article_content", "article_img", "category")

# comments


class CommentsSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField()

    def get_user(self, obj):
        return obj.user.nickname

    class Meta:
        model = Comments
        exclude = ('article',)  # 게시글 필드 빼고 보여주기


# comments작성
class CommentsCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comments
        fields = ("comment",)


#
