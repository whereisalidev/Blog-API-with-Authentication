from django.urls import path
from .views import BlogAPI

urlpatterns = [
    path('', BlogAPI.as_view())
]
