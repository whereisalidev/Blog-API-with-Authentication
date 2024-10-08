from django.shortcuts import render
from django.contrib.auth.models import User
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import RegisterSerializer, LoginSerializer
# from rest_framework.authtoken.models import Token
from rest_framework_simplejwt.tokens import RefreshToken


class RegisterAPI(APIView):
    def post(self, request):
        data = request.data
        serializer = RegisterSerializer(data=data)
        if not serializer.is_valid():
            return Response({'message': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        serializer.save()
        return Response({'message': 'User Registered Successfully'}, status=status.HTTP_201_CREATED)
    
class LoginAPI(APIView):
    def post(self, request):
        data = request.data
        serializer = LoginSerializer(data=data)
        if not serializer.is_valid():
            return Response({'message': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        user = User.objects.get(email=data['email'])
        refresh = RefreshToken.for_user(user)
        return Response({
            'message': 'User login Successfully',
            # 'refresh': str(refresh),
            'token': str(refresh.access_token),
        }, status=status.HTTP_200_OK)
