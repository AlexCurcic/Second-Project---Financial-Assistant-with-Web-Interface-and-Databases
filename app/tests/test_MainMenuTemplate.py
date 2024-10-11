from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse
from bs4 import BeautifulSoup
from ..views import *




class MainMenuTemplateTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')

    def test_main_menu_links_authenticated(self):
        client = Client()
        client.force_login(self.user)
        main_menu_url = reverse('main_menu')
        response = client.get(main_menu_url)
        self.assertEqual(response.status_code, 200)
        soup = BeautifulSoup(response.content, 'html.parser')
        list_group = soup.find('ul', class_='list-group')
        links = list_group.find_all('a')
        expected_links = [
            reverse('operations'), reverse('currency_exchange'), reverse('history')
        ]
        self.assertEqual(len(set(links)), 3)
        for link in links:
            self.assertIn(link['href'], expected_links)