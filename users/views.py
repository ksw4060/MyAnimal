from django.shortcuts import render
from rest_framework.views import APIView
from users.serializers import UserSerializer, CustomTokenObtainPairSerializer

# Create your views here.

# 로그인, 회원가입 - 김성우
#


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
