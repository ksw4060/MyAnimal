from django.urls import path
from users import views
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    path('signup/', views.SignupView.as_view(), name='sign_up_view'),
    path('login/', views.CustomTokenObtainPairView.as_view(), name='login_view'),
    path("refresh/", TokenRefreshView.as_view(), name="token_refresh"),


    path('profile/<int:user_id>', views.ProfileView.as_view(), name="profile_view"),
    path('follow/<int:user_id>/', views.FollowView.as_view(), name='follow_view'),
    path('signup/', views.SignupView.as_view(), name='sign_up_view'),
    path('login/', views.CustomTokenObtainPairView.as_view(), name='login_view'),
]
