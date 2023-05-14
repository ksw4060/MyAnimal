from base64 import urlsafe_b64decode, urlsafe_b64encode
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.contrib.auth import authenticate
from django.utils.http import urlsafe_base64_decode
from django.utils.encoding import DjangoUnicodeDecodeError, force_str, force_bytes
from django.db.models.query_utils import Q
from django.shortcuts import render
from django.core.mail import EmailMessage

from rest_framework.authtoken.models import Token
from rest_framework import status, permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.generics import get_object_or_404
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.generics import CreateAPIView
from rest_framework.parsers import MultiPartParser, FormParser


from users.serializers import UserSerializer, CustomTokenObtainPairSerializer, UserProfileSerializer
from .serializers import PasswordResetSerializer, SetNewPasswordSerializer, TokenSerializer, EmailThread, PasswordVerificationSerializer

from .models import Users


# from .models import Image
# from .serializers import ImageSerializer

# 로그인, 회원가입 - 김성우

# 회원가입
class Util:

    @staticmethod
    def send_email(message):
        email = EmailMessage(subject=message["email_subject"], body=message["email_body"], to=[
                             message["to_email"]])
        EmailThread(email).start()


class SignupView(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            user.is_active = False
            user = serializer.save()

            # 토큰 생성

            uid = urlsafe_b64encode(force_bytes(user.pk))
            token = PasswordResetTokenGenerator().make_token(user)

            # 이메일 전송

            email = user.email
            authurl = f'http://localhost:8000/users/verify-email/{uid}/{token}/'
            email_body = "이메일 인증" + authurl
            message = {
                "email_body": email_body,
                "to_email": email,
                "email_subject": "이메일 인증",
            }
            Util.send_email(message)

            return Response({"message": "가입완료!"}, status=status.HTTP_201_CREATED)
        else:
            return Response({"message": f"${serializer.errors}"}, status=status.HTTP_400_BAD_REQUEST)


class VerifyEmailView(APIView):
    def get(self, request, uidb64, token):
        try:
            # URL에 포함된 uid를 디코딩하여 사용자 식별
            uid = urlsafe_base64_decode(uidb64).decode()
            user = Users.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, Users.DoesNotExist):
            user = None

        token_generator = PasswordResetTokenGenerator()
        # 사용자가 존재하고 토큰이 유효한지 확인
        if user is not None and token_generator.check_token(user, token):
            # 이메일 인증 완료 처리
            user.is_active = True
            user.save()
            return Response({"message": "이메일 인증이 완료되었습니다."}, status=status.HTTP_200_OK)
        else:
            return Response({"message": "잘못된 링크입니다."}, status=status.HTTP_400_BAD_REQUEST)


# 로그인
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
        if user == request.user:
            serializer = UserProfileSerializer(
                user, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response({"message": "수정완료!"}, status=status.HTTP_200_OK)
            else:
                return Response({"message": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"message": "권한이 없습니다!"}, status=status.HTTP_403_FORBIDDEN)
# 이미지 업로드, 교체 가능, 삭제는 없음.


# 회원탈퇴 - 0514 준영 추가 =================================================================
class WithdrawalView(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request):
        serializer = PasswordVerificationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = request.user
        password = serializer.validated_data['password']

        # 비밀번호 검증 로직을 작성합니다.
        if user.check_password(password):
            # request.user.is_active = False  # 사용자 비활성화
            # request.user.save()
            user.delete() # 사용자 삭제
            return Response({'message': '탈퇴가 성공적으로 처리되었습니다.'}, status=status.HTTP_200_OK)
        else:
            return Response({'message': '비밀번호가 일치하지 않습니다.'}, status=status.HTTP_400_BAD_REQUEST)



# ========================== 팔로우 =====================================
class FollowView(APIView):
    # permission_classes = [IsAuthenticated]

    def get(self, request, user_id):
        you = get_object_or_404(Users, id=user_id)
        serializer = UserProfileSerializer(you)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, user_id):
        you = get_object_or_404(Users, id=user_id)
        me = request.user
        if me.is_authenticated:
            # 채연수정 : 현재 로그인한 유저와 팔로우 대상이 다를경우 (내가 아닌 경우에만 팔로우)
            if you != request.user:

                if me in you.followers.all():
                    you.followers.remove(me)
                    return Response("unfollow했습니다.", status=status.HTTP_200_OK)
                else:
                    you.followers.add(me)
                    return Response("follow했습니다.", status=status.HTTP_200_OK)
            else:
                return Response("로그인이 필요합니다.", status=status.HTTP_403_FORBIDDEN)
        else:
            return Response("", status=status.HTTP_400_BAD_REQUEST)

# 로그인 한 유저만 팔로우 할 수 있게 수정함.


# 비밀번호 찾기 (이메일 보내기)
class PasswordResetView(APIView):

    def post(self, request):
        serializer = PasswordResetSerializer(data=request.data)
        if serializer.is_valid():
            return Response({"message": "비밀번호 재설정 이메일"}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# 비밀번호 재설정 토큰 확인
class PasswordTokenCheckView(APIView):

    def get(self, request, uidb64, token):
        try:
            user_id = force_str(urlsafe_b64decode(uidb64))
            user = get_object_or_404(Users, id=user_id)
            if not PasswordResetTokenGenerator().check_token(user, token):
                return Response({"message": "링크가 유효하지 않습니다."}, status=status.HTTP_401_UNAUTHORIZED)

            return Response({"uidb64": uidb64, "token": token}, status=status.HTTP_200_OK)

        except DjangoUnicodeDecodeError as identifier:
            return Response({"message": "링크가 유효하지 않습니다."}, status=status.HTTP_401_UNAUTHORIZED)


# 비밀번호 재설정
class SetNewPasswordView(APIView):

    def put(self, request):
        serializer = SetNewPasswordSerializer(data=request.data)
        if serializer.is_valid():
            return Response({"message": "비밀번호 재설정 완료"}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# 회원정보 인증 토큰 발급
class ObtainUserTokenView(APIView):

    def post(self, request):
        serializer = TokenSerializer(
            data=request.data, context={"request": request})
        if serializer.is_valid():
            user = authenticate(
                email=serializer.validated_data["email"],
                password=serializer.validated_data["password"],
            )
            token, _ = Token.objects.get_or_create(user=user)
            return Response({"token": token.key}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# # ========================== 이미지 뷰 =====================================
# class ImageView(CreateAPIView):
#     queryset = Image.objects.all()
#     serializer_class = ImageSerializer
#     parser_classes = (MultiPartParser, FormParser)
