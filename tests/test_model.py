from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth.models import User
from blog.models import Blog


class BlogTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='password')
        self.client.login(username='testuser', password='password')
        self.blog_data = {
            'title': 'Test Blog',
            'description': 'This is a test blog',
            'image': None,  # Assuming no image for simplicity in this example
        }
        self.blog = Blog.objects.create(user=self.user, **self.blog_data)

    def test_create_blog(self):
        url = reverse('blog-list')
        response = self.client.post(url, self.blog_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Blog.objects.count(), 2)

    def test_retrieve_blog(self):
        url = reverse('blog-detail', kwargs={'pk': self.blog.pk})
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], self.blog_data['title'])

    def test_update_blog(self):
        url = reverse('blog-detail', kwargs={'pk': self.blog.pk})
        updated_data = self.blog_data.copy()
        updated_data['title'] = 'Updated Test Blog'
        response = self.client.put(url, updated_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.blog.refresh_from_db()
        self.assertEqual(self.blog.title, 'Updated Test Blog')

    def test_delete_blog(self):
        url = reverse('blog-detail', kwargs={'pk': self.blog.pk})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Blog.objects.count(), 0)
