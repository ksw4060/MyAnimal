from . import views
from django.urls import path


urlpatterns = [
    path('/articles/<int:article_id>/hearts/', views.HeartsView.as_view(), name='Hearts_View'), # 좋아요 기능 url
]