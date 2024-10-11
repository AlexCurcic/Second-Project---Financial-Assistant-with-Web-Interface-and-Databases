from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse 
from ..views import *

class MainMenuViewTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.main_menu_url = reverse('main_menu') 

    def test_main_menu_view_get_authenticated(self):
        user = User.objects.create_user(username='testuser', password='testpassword')
        self.client.force_login(user)
        response = self.client.get(self.main_menu_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'app/main_menu.html')
        self.assertEqual(response.context['username'], 'testuser')

    def test_main_menu_view_get_unauthenticated(self):
        response = self.client.get(self.main_menu_url)
        self.assertEqual(response.status_code, 302) 

