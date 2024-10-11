from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse
from ..views import *

class CurrencyExchangeViewTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.exchange_url = reverse('currency_exchange')

    def test_currency_exchange_view_get(self):
        user = User.objects.create_user(username='testuser', password='testpassword')
        self.client.force_login(user)
        response = self.client.get(self.exchange_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'app/currency_exchange.html')
        self.assertIn('currency_choices', response.context)
        self.assertIsNone(response.context['amount'])
        self.assertIsNone(response.context['currency'])
        self.assertIsNone(response.context['exchanged_amount'])

    def test_currency_exchange_view_post_with_data(self):
        user = User.objects.create_user(username='testuser', password='testpassword')
        self.client.force_login(user)
        response = self.client.post(self.exchange_url, {'amount': 100, 'currency': 'USD'})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'app/currency_exchange.html')
        self.assertIn('currency_choices', response.context)
        self.assertEqual(response.context['amount'], 100)
        self.assertEqual(response.context['currency'], 'USD')
        self.assertIsNotNone(response.context['exchanged_amount'])
        self.assertIsInstance(response.context['exchanged_amount'], float)

    def test_currency_exchange_view_post_invalid_amount(self):
        user = User.objects.create_user(username='testuser', password='testpassword')
        self.client.force_login(user)
        response = self.client.post(self.exchange_url, {'amount': 'invalid', 'currency': 'USD'})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'app/currency_exchange.html')
        self.assertIn('currency_choices', response.context)
        self.assertIsNone(response.context['amount'])
        self.assertIsNone(response.context['currency'])
        self.assertIsNone(response.context['exchanged_amount'])