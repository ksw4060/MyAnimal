from rest_framework import serializers
from articles.models import Articles, Comments, ArticleImage


# articles

# 이미지 업로드 시리얼라이저 - 이미지 직렬화
class ArticleImageSerializer(serializers.ModelSerializer):
    image = serializers.ImageField(use_url=True)

    class Meta:
        model = ArticleImage
        fields = ['image']
        
class ArticlesSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField()
    images = serializers.ListField(child=serializers.ImageField())

    def get_user(self, obj):
        return obj.user.email
    
    #게시글에 등록된 이미지들 가지고 오기
    def get_images(self, obj):
        image = obj.image.all() 
        return ArticleImageSerializer(instance=image, many=True, context=self.context).data


class ArticlesCreateSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField()

    class Meta:
        model = Articles
        fields = '__all__'

    def get_user(self, obj):
        return obj.user.email


# comments
class CommentsSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField()

    def get_user(self, obj):
        return obj.user.email

    class Meta:
        model = Comments
        exclude = ('article',)  # 게시글 필드 빼고 보여주기


# comments작성
class CommentsCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comments
        fields = ("comment",)


#
