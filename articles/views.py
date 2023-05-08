from rest_framework.views import APIView
from rest_framework.generics import get_object_or_404
from rest_framework import status, permissions
from rest_framework.response import Response
from articles.models import Articles
from articles.serializers import ArticlesSerializer,ArticlesCreateSerializer
import datetime



# ============================ 글 목록, 작성 클래스 (id 불필요) ============================  

class ArticlesView(APIView): # /articles/
    pass


# ============================ 글 상세, 수정 클래스 (id 필요) ============================ 
class ArticlesDetailView(APIView): # /todo/id/
    
     # =================== 글 상세 =================== 
    
    def get(self, request,todo_id): # => request.method == 'GET':
        articles = get_object_or_404(Articles,id=todo_id)

        serializer = ArticlesSerializer(articles)
        return Response(serializer.data, status=status.HTTP_200_OK)
        
            
    # =================== 글 수정 =================== 
    
    def patch(self, request,todo_id): # => request.method == 'PATCH':
        articles = get_object_or_404(Articles,id=todo_id) # db 불러오기
        # 로그인된 사용자의 글일때만
        if request.user == articles.user:
            serializer = ArticlesCreateSerializer(articles, data=request.data) 
            
            # 유효성검사를 통과하면
            if serializer.is_valid(): 
                articles.updated_at = datetime.datetime.now() # 업데이트 시간 
                # is_complete == True 이고 completea_at 필드가 비어있다면 --> 완료된 todo로 수정하면 (이미 완료된 todo를 수정했을 때는 시간이 업데이트 되지 않음)
                serializer.save(user=request.user) # db에 저장
                return Response(serializer.data,status=status.HTTP_201_CREATED)
            else: # 유효성검사를 통과하지 못하면
                return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)