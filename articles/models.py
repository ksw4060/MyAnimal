from django.db import models
from users.models import Users

# Create your models here.


class Articles(models.Model):
    class Meta:
        db_table = "Article"
        ordering = ['-article_created_at']  # 게시글 최신순 정렬

    user = models.ForeignKey(Users, on_delete=models.CASCADE)
    article_title = models.CharField("글제목", max_length=45)
    article_content = models.TextField("글내용")
    article_img = models.FileField(
        "이미지", upload_to='', blank=True, null=True)  # 글 내 이미지 업로드
    article_created_at = models.DateTimeField(auto_now_add=True)  # 생성시각
    article_updated_at = models.DateTimeField(
        auto_now=True, null=True, blank=True)  # 수정시각
    '''
    수정 시각은 최초 글 작성시 디폴트를 None 으로, 수정시에 수정 시각 업데이트 되는 것으로 하겠습니다.
    '''
    categories = (
        ('cat', '고양이'),
        ('dog', '개'),
        ('bird', '새'),
        ('fish', '물고기'),
        ('snail', '달팽이'),
        ('stone', '돌'),
        ('turtle', '거북이'),
    )
    category = models.CharField("반려동물 종류", choices=categories, max_length=10)

    # 좋아요 : 게시글과 사용자를 연결하는 Many To Many 필드입니다.
    hearts = models.ManyToManyField(Users, blank=True, related_name='hearts')
    # 북마크 : 게시글과 사용자를 연결하는 Many To Many 필드입니다.
    bookmarks = models.ManyToManyField(
        Users, blank=True, related_name='bookmarks')

    def __str__(self):
        return str(self.article_title)

    # 좋아요 갯수 세는 함수
    def count_hearts(self):
        return self.hearts.count()

    # 북마크 갯수 세는 함수
    def count_bookmarks(self):
        return self.bookmarks.count()


'''
이미지 다중 업로드 받기
- 게시글과 이미지를 1:N으로 설정해 테이블 생성
'''

# 이미지 업로드 경로
# def image_upload_path(instance, filename):
#     return f'{instance.article.id}/{filename}'

# class ArticleImage(models.Model):
#     article = models.ForeignKey(Articles, on_delete=models.CASCADE, related_name='image')
#     image = models.ImageField(upload_to=image_upload_path)

#     def __int__(self):
#         return self.id

#     class Meta:
#         db_table = 'article_image'


# 댓글 models
class Comments(models.Model):
    class Meta:
        db_table = 'comment'
        ordering = ['-comment_created_at']  # 게시글 최신순 정렬

    user = models.ForeignKey(Users, on_delete=models.CASCADE)
    article = models.ForeignKey(
        Articles, on_delete=models.CASCADE, related_name="comments")
    comment = models.TextField("댓글")
    comment_created_at = models.DateTimeField(auto_now_add=True)  # 생성시각
    # 수정시각, 최초 글 작성시 디폴트를 None 으로, 수정시에 수정 시각 업데이트
    comment_updated_at = models.DateTimeField(
        auto_now=True, null=True, blank=True)

    def __str__(self):
        return str(self.comment)
