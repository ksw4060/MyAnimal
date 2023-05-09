from . import views
from django.urls import path


urlpatterns = [

    path('', views.ArticlesView.as_view(), name='article'),
    path('<int:article_id>', views.ArticlesView.as_view(), name='article'),

    path('<int:article_id>/hearts/', views.HeartsView.as_view(),
         name='Hearts_View'),  # 좋아요 기능
    path('<int:user_id>/hearts/', views.HeartsView.as_view(),
         name='User_Hearts_View'),  # 좋아요 한 게시글

    path('<int:article_id>/bookmarks/', views.BookMarksView.as_view(),
         name='bookmarks_View'),  # 북마크 기능
    path('<int:user_id>/bookmarks/', views.BookMarksView.as_view(),
         name='bookmarks_View'),  # 북마크 한 게시글

    path('<int:article_id>/comment/', views.CommentsView.as_view(),
         name="comment_view"),  # 댓글 보기랑 작성
    path('<int:article_id>/comment/<int:comment_id>/',
         views.CommentsdetailView.as_view(), name="comment_detail_view"),  # 댓글 수정과 삭제

]
