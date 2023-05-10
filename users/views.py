from .models import Users
from rest_framework import status, permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.generics import get_object_or_404
from rest_framework_simplejwt.views import TokenObtainPairView
from django.shortcuts import render
from users.serializers import UserSerializer, CustomTokenObtainPairSerializer, UserProfileSerializer

from django.db.models.query_utils import Q

from rest_framework.generics import CreateAPIView
from rest_framework.parsers import MultiPartParser, FormParser
from .models import Image
from .serializers import ImageSerializer
# 로그인, 회원가입 - 김성우


class SignupView(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "가입완료!"}, status=status.HTTP_201_CREATED)
        else:
            return Response({"message": f"${serializer.errors}"}, status=status.HTTP_400_BAD_REQUEST)


class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer


# ====================== 프로필 상세보기 ================================
class ProfileView(APIView):
    def get_object(self, user_id):
        return get_object_or_404(Users, id=user_id)

    # 프로필 상세보기, 권한이 없어도 됨.
    def get(self, request, user_id):
        user = self.get_object(user_id)
        serializer = UserProfileSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)

    # 프로필 수정, 권한이 있어야함.
    def patch(self, request, user_id):
        user = self.get_object(user_id)
        print(f"{request.data=}")
        if user == request.user:
            serializer = UserProfileSerializer(
                user, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                print(f"{serializer.data=}")
                return Response({"message": "수정완료!"}, status=status.HTTP_200_OK)
            else:
                return Response({"message": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"message": "권한이 없습니다!"}, status=status.HTTP_403_FORBIDDEN)
# 작성자 - 이준영
# 이미지 업로드, 교체 가능, 삭제는 없음.


# ========================== 팔로우 =====================================
class FollowView(APIView):
    # 팔로우 - 이준영
    # permission_classes = [IsAuthenticated]

    def post(self, request, user_id):
        you = get_object_or_404(Users, id=user_id)
        me = request.user
        if me.is_authenticated:
            if me in you.followers.all():
                you.followers.remove(me)
                return Response("unfollow했습니다.", status=status.HTTP_200_OK)
            else:
                you.followers.add(me)
                return Response("follow했습니다.", status=status.HTTP_200_OK)
        else:
            return Response("로그인이 필요합니다.", status=status.HTTP_403_FORBIDDEN)
# 로그인 한 유저만 팔로우 할 수 있게 수정함.


# ========================== 이미지 뷰 =====================================
class ImageView(CreateAPIView):
    queryset = Image.objects.all()
    serializer_class = ImageSerializer
    parser_classes = (MultiPartParser, FormParser)
