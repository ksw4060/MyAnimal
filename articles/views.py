from rest_framework.views import APIView
from rest_framework.generics import get_object_or_404
from .models import Articles
from rest_framework.response import Response
from rest_framework import status
# Create your views here.

class HeartsView(APIView):
    def post(self,request, article_id):
        article = get_object_or_404(Articles, id=article_id)
        if request.user in article.hearts.all():
            article.hearts.remove(request.user)
            return Response('좋아요 취소', status=status.HTTP_200_OK)
        else:
            article.hearts.add(request.user)
            return Response('좋아요', status=status.HTTP_200_OK)