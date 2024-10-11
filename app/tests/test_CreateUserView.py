from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse
from unittest.mock import patch
from ..views import *
from ..forms import CreateUserForm

class CreateUserViewTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.create_user_url = reverse('create_account')

    def test_create_user_view_get(self):
        response = self.client.get(self.create_user_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'app/create_account.html')
        self.assertIsInstance(response.context['form'], CreateUserForm)

    @patch('app.views.User.objects.create_user')
    def test_create_user_view_post(self, mock_create_user):
        mock_create_user.return_value = User.objects.create_user(username='testuser', password='testpassword')
        data = {
            'username': 'testuser',
            'password1': 'testpassword',
            'password2': 'testpassword',
        }
        response = self.client.post(self.create_user_url, data)
        self.assertRedirects(response, reverse('login'))
        self.assertTrue(User.objects.filter(username='testuser').exists())

    def test_create_user_view_context_authenticated(self):
        user = User.objects.create_user(username='testuser', password='testpassword')
        self.client.force_login(user)
        response = self.client.get(self.create_user_url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['username'], 'testuser')