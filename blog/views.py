from django.shortcuts import render
from .serializers import BlogSerializer, AllBlogsSerializer
from .models import Blog
from django.db.models import Q
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication



class BlogAPI(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def get(self, request):
        try:
            blogs = Blog.objects.filter(user = request.user)
            # if request.GET.get('search'):
            #     search = request.GET.get('search')
            #     blogs = blogs.filter(Q(title__icontains = search))
            serializer = BlogSerializer(blogs, many=True)
            return Response({'message': f'Blogs fetched successfully for {request.user}', 'data': serializer.data}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'data': str(e)}, status=status.HTTP_400_BAD_REQUEST)

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
        
    def patch(self, request):
        try:
            data = request.data
            blog = Blog.objects.filter(uuid = data.get['uuid'])

            if not blog.exists():
                return Response({'message': 'Invalid Blog UUID'}, status=status.HTTP_400_BAD_REQUEST)
            
            if request.user != blog[0].user:
                return Response({'message': 'You are not Authorized for this updation'}, status=status.HTTP_401_UNAUTHORIZED)
            
            serializer = BlogSerializer(blog[0], data = data, partial = True)

            if not serializer.is_valid():
                return Response({'message': 'Something went wrong', 'data': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
            
            serializer.save()

            return Response({'message': ' Blog updated Successfully', 'data': serializer.data}, status=status.HTTP_201_CREATED)

        except Exception as e:
            print(f'Exception {e}')
            return Response({'data': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        

class AllBlogsAPI(APIView):
    def get(self, request):
        blogs = Blog.objects.all()
        if request.GET.get('search'):
                search = request.GET.get('search')
                blogs = blogs.filter(Q(title__icontains = search))
        serializer = AllBlogsSerializer(blogs, many=True)
        return Response(serializer.data)