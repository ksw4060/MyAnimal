from django.urls import path
from users import views

urlpatterns = [
    path('profile/<int:user_id>', views.ProfileView.as_view(), name="profile_view"),
    path('follow/<int:user_id>/', views.FollowView.as_view(), name='follow_view'),
    path('signup/', views.SignupView.as_view(), name='sign_up_view'),
    path('login/', views.CustomTokenObtainPairView.as_view(), name='login_view'),
]
