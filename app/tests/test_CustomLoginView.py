from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse 
from ..views import *

class CustomLoginViewTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.login_url = reverse('login')

    def test_login_view_get(self):
        response = self.client.get(self.login_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'app/login.html')

    def test_login_view_post_success(self):
        user = User.objects.create_user(username='testuser', password='testpassword')
        data = {
            'username': 'testuser',
            'password': 'testpassword',
        }
        response = self.client.post(self.login_url, data)
        self.assertRedirects(response, reverse('main_menu'))

    def test_login_view_post_invalid_credentials(self):
        data = {
            'username': 'invaliduser',
            'password': 'invalidpassword',
        }
        response = self.client.post(self.login_url, data)
        self.assertEqual(response.status_code, 200) 
        self.assertContains(response, 'Please enter a correct username and password.')

    def test_login_view_context_authenticated(self):
        user = User.objects.create_user(username='testuser', password='testpassword')
        self.client.force_login(user)
        response = self.client.get(self.login_url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['username'], 'testuser')