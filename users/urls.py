from django.urls import path
from users import views
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    path('signup/', views.SignupView.as_view(),
         name='sign_up_view'),  # /users/signup/
    path('login/', views.CustomTokenObtainPairView.as_view(),
         name='login_view'),  # /users/login/
    path("refresh/", TokenRefreshView.as_view(),
         name="token_refresh"),  # /users/refresh/

    path("auth/password/reset/", views.PasswordResetView.as_view(),
         name="password_reset"),  # 비밀번호 찾기 (이메일 보내기)
    path("auth/password/reset/b'<str:uidb64>'/<str:token>/",
         views.PasswordTokenCheckView.as_view(), name="password_reset_confirm"),  # 비밀번호 재설정 토큰 확인
    path("auth/password/reset/confirm/", views.SetNewPasswordView.as_view(),
         name="password_reset_confirm"),  # 비밀번호 재설정

    path("verify-email/b'<str:uidb64>'/<str:token>/",
         views.VerifyEmailView.as_view(), name='verify-email'),

]
