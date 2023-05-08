from .models import Users
from rest_framework import status, permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.generics import get_object_or_404


# 로그인, 회원가입 - 김성우
#

# 프로필 - 이준영
class ProfileView(APIView):
    def get_object(self, user_id):
        return get_object_or_404(Users, id=user_id)

    # 프로필 상세보기, 권한이 없어도 됨.
    def get(self, requset, user_id):
        pass

    # 프로필 수정, 권한이 있어야함.
    def patch(self, request, user_id):
        user = self.get_object(user_id)
        if user == request.id:
            pass
        pass
