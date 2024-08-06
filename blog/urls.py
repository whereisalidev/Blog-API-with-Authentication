from django.urls import path
from .views import BlogAPI, AllBlogsAPI

urlpatterns = [
    path('', BlogAPI.as_view()),
    path('all', AllBlogsAPI.as_view() )
]
