from django.shortcuts import render
from .serializers import BlogSerializer
from .models import Blog
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication



class BlogAPI(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    
    def post(self, request):
        try:
            data = request.data
            data['user'] = request.user.id
            serializer = BlogSerializer(data=data)
            if not serializer.is_valid():
                return Response({'data': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
            serializer.save()
            return Response({'message': 'Blog Created successfully', 'id': serializer.data['uuid']}, status=status.HTTP_201_CREATED)
        except Exception as e:
            print(f'Exception {e}')
            return Response({'data': str(e)}, status=status.HTTP_400_BAD_REQUEST)


class AllBlogsAPI(APIView):
    def get(self, request):
        blogs = Blog.objects.all()
        serializer = BlogSerializer(blogs, many=True)
        return Response({serializer.data})