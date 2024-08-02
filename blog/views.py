from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from .serializers import BlogSerializer




class BlogAPI(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request):
        data = request.data
        serializer = BlogSerializer(data=data)
