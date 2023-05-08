from rest_framework.views import APIView
from rest_framework.generics import get_object_or_404
from rest_framework import status
from rest_framework.response import Response
from articles.models import Articles
from articles.serializers import ArticlesSerializer,ArticlesCreateSerializer
import datetime


# ============================ 글 목록, 작성 클래스 (id 불필요) ============================  

class ArticlesView(APIView): # /articles/
    
    # =================== 글 목록 =================== 
    
    def get(self, request): # => request.method == 'GET':
        articles = Articles.objects.all()
        serializer = ArticlesSerializer(articles, many=True)
        return Response (serializer.data, status=status.HTTP_200_OK)
            
    # =================== 글 작성 =================== 
    
    def post(self, request): # => request.method == 'POST':
        serializer = ArticlesCreateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
   


# ============================ 글 상세, 수정 클래스 (id 필요) ============================ 
class ArticlesDetailView(APIView): # /articles/id/
    
     # =================== 글 상세 =================== 
    
    def get(self, request,article_id): # => request.method == 'GET':
        articles = get_object_or_404(Articles,id=article_id)
        serializer = ArticlesSerializer(articles)
        return Response(serializer.data, status=status.HTTP_200_OK)
        
            
    # =================== 글 수정 =================== 
    
    def patch(self, request,article_id): # => request.method == 'PATCH':
        articles = get_object_or_404(Articles,id=article_id) # db 불러오기
        # 로그인된 사용자의 글일때만
        if request.user == articles.user:
            serializer = ArticlesCreateSerializer(articles, data=request.data) 
            
            # 유효성검사를 통과하면
            if serializer.is_valid(): 
                articles.updated_at = datetime.datetime.now() # 업데이트 시간 

                serializer.save(user=request.user) # db에 저장
                return Response(serializer.data,status=status.HTTP_201_CREATED)
            else: # 유효성검사를 통과하지 못하면
                return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
            
      # =================== 글 삭제 =================== 
    
    def delete(self, request,article_id): # => request.method == 'DELETE':
        articles = Articles.objects.get(id=article_id) # db 불러오기
        if request.user == articles.user: # 로그인된 사용자의 글일때만
            articles.delete() # 삭제
            return Response({"message":"삭제완료!"},status=status.HTTP_204_NO_CONTENT)
        else: # 로그인된 사용자의 글이 아니라면 
            return Response({"message":"권한이 없습니다"},status=status.HTTP_403_FORBIDDEN)


# 게시글 좋아요 기능.
class HeartsView(APIView):
    def post(self,request, article_id):
        article = get_object_or_404(Articles, id=article_id)
        if request.user in article.hearts.all():
            article.hearts.remove(request.user)
            return Response('좋아요 취소', status=status.HTTP_200_OK)
        else:
            article.hearts.add(request.user)
            return Response('좋아요', status=status.HTTP_200_OK)
            