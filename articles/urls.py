from . import views
from django.urls import path


urlpatterns = [

    path('',views.ArticlesView.as_view(), name = 'article'), # /articles/
    path('<int:article_id>/',views.ArticlesDetailView.as_view(), name = 'article'), # /articles/<int:article_id>/
    

    path('<int:article_id>/hearts/', views.HeartsView.as_view(), name='Hearts_view'),  # 좋아요 기능
    path('hearts/',views.HeartsView.as_view(), name='User_Hearts_View'), # 좋아요 한 게시글
  
    path('<int:article_id>/bookmarks/',views.BookMarksView.as_view(), name='bookmarks_View'),  # 북마크 기능
    path('bookmarks/',views.BookMarksView.as_view(), name='bookmarks_View'),  # 북마크 한 게시글

  
    path('<int:article_id>/comment/', views.CommentsView.as_view(), name="comment_view"), # /articles/<int:article_id>/comment/
    path('<int:article_id>/comment/<int:comment_id>/',views.CommentsdetailView.as_view(), name="comment_detail_view"), # /articles/<int:article_id>/comment/<int:comment_id>/

]
