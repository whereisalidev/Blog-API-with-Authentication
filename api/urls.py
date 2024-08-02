from django.urls import path, include


urlpatterns = [
    path('auth/', include('account.urls')),
    path('blog/', include('blog.urls')),
]
