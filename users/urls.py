from django.urls import path
from users import views

urlpatterns = [
    path('profile/<int:user_id>', views.ProfileView.as_view(), name="profile_view"),
    path('follow/<int:user_id>/', views.FollowView.as_view(), name='follow_view'),
]
