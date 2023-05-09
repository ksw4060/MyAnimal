from . import views
from django.urls import path


urlpatterns = [
    path('articles/',views.ArticlesView.as_view(), name = 'article'),
    path('articles/<int:article_id>',views.ArticlesView.as_view(), name = 'article'),
    
    path('articles/<int:article_id>/hearts/',views.HeartsView.as_view(), name='Hearts_View'),  # 좋아요 기능 url
    
    path('<int:article_id>/comment/',views.CommentsView.as_view(), name="comment_view"),
    path('<int:article_id>/comment/<int:comment_id>/',views.CommentsdetailView.as_view(), name="comment_detail_view"),
]
