from rest_framework.views import APIView
from rest_framework.generics import get_object_or_404
from rest_framework import status
from rest_framework.response import Response
from articles.models import Articles, Comments
from articles.serializers import ArticlesSerializer, CommentsSerializer, CommentsCreateSerializer
import datetime


# ============================ 글 목록, 작성 클래스 (id 불필요) ============================


class ArticlesView(APIView):  # /articles/

    # =================== 글 목록 ===================

    def get(self, request):  # => request.method == 'GET':
        articles = Articles.objects.all()
        serializer = ArticlesSerializer(articles, many=True)
        return Response (serializer.data, status=status.HTTP_200_OK)
            
    # =================== 글 작성 =================== 
    
    def post(self, request): # => request.method == 'POST':
        serializer = ArticlesSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



# ============================ 글 상세, 수정 클래스 (id 필요) ============================ 
class ArticlesDetailView(APIView): # /articles/id/
    
     # =================== 글 상세 =================== 
    
    def get(self, request,article_id): # => request.method == 'GET':
        articles = get_object_or_404(Articles,article_id=article_id)
        serializer = ArticlesSerializer(articles)
        return Response(serializer.data, status=status.HTTP_200_OK)

    # =================== 글 수정 ===================

    def patch(self, request, article_id):  # => request.method == 'PATCH':
        articles = get_object_or_404(Articles, id=article_id)  # db 불러오기
        # 로그인된 사용자의 글일때만
        if request.user == articles.user:
            serializer = ArticlesSerializer(articles, data=request.data) 
            
            # 유효성검사를 통과하면
            if serializer.is_valid():
                articles.updated_at = datetime.datetime.now()  # 업데이트 시간

                serializer.save(user=request.user)  # db에 저장
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            else:  # 유효성검사를 통과하지 못하면
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

      # =================== 글 삭제 ===================

    def delete(self, request, article_id):  # => request.method == 'DELETE':
        articles = Articles.objects.get(id=article_id)  # db 불러오기
        if request.user == articles.user:  # 로그인된 사용자의 글일때만
            articles.delete()  # 삭제
            return Response({"message": "삭제완료!"}, status=status.HTTP_204_NO_CONTENT)
        else:  # 로그인된 사용자의 글이 아니라면
            return Response({"message": "권한이 없습니다"}, status=status.HTTP_403_FORBIDDEN)


# ====================== 게시글 좋아요 ================================
class HeartsView(APIView):
    def post(self,request, article_id):
        article = get_object_or_404(Articles, id=article_id)
        if request.user in article.hearts.all():
            article.hearts.remove(request.user)
            return Response('좋아요 취소', status=status.HTTP_200_OK)
        else:
            article.hearts.add(request.user)
            return Response('좋아요', status=status.HTTP_200_OK)
        
    
# ====================== 좋아요 한 게시글 보기 ================================
    def get(self,request):
        user = request.user
        article = user.hearts.all()
        serializer = ArticlesSerializer(article, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

# ====================== 게시글 북마크 ================================
class BookMarksView(APIView):
    def post(self, request, article_id):
        articles = get_object_or_404(Articles, id=article_id)
        if request.user in articles.bookmarks.all():
            articles.bookmarks.remove(request.user)
            return Response('북마크 취소', status=status.HTTP_200_OK)
        else:
            articles.bookmarks.add(request.user)
            return Response('북마크', status=status.HTTP_200_OK)
        
# ====================== 북마크 한 게시글 보기 ================================
    def get(self,request):
        user = request.user
        article = user.bookmarks.all()
        serializer = ArticlesSerializer(article, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

# ====================== 댓글 목록, 작성 클래스 ================================

class CommentsView(APIView):  # <int:article_id>/comment/

    # ===================== 댓글 목록 보기 =========================

    def get(self, request, article_id):
        article = get_object_or_404(Articles, id=article_id)
        comments = article.comments.all()  # 게시글에 작성한 모든 쿼리셋들을 불러옴
        serializer = CommentsSerializer(comments, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
        # return Response({"연결완료!"})#urls연결확인

    # ======================== 댓글 작성 ============================

    def post(self, request, article_id):
        serializer = CommentsCreateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user, article_id=article_id)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# ========================= 댓글 수정 및 삭제 (id 확인) ==============================

class CommentsdetailView(APIView):  # <int:article_id>/comment/<int:comment_id>/

    # ===================== 댓글 수정 =================================

    def put(self, request, article_id, comment_id):
        comment = get_object_or_404(Comments, id=comment_id)
        if request.user == comment.user:
            serializer = CommentsCreateSerializer(comment, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response("권한이 없습니다!", status=status.HTTP_403_FORBIDDEN)
        # return Response({"연결성공"}) #url연결성공
        # 로그인을 안해서 그런지 권한이 없습니다! 라는 문구가 생성

    # ===================== 댓글 삭제 =================================
    def delete(self, request, article_id, comment_id):
        comment = get_object_or_404(Comments, id=comment_id)
        if request.user == comment.user:
            comment.delete()
            return Response("삭제되었습니다!", status=status.HTTP_204_NO_CONTENT)
        else:
            return Response("권한이 없습니다!", status=status.HTTP_403_FORBIDDEN)
        # 로그인을 안해서 그런지 권한이 없습니다! 라는 문구가 생성

            