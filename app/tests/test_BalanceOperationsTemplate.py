from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse
from ..models import History  
from ..views import *




class BalanceOperationsTemplateTestCase(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')


    def test_balance_operations_balance_nonzero(self):
        client = Client()
        History.objects.create(status='success', amount=100, type='deposit', user=self.user)
        History.objects.create(status='failure', amount=50, type='withdraw', user=self.user)
        client.force_login(self.user)
        balance_operations_url = reverse('operations')
        response = client.get(balance_operations_url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, f'Your current balance: ${100}')

    def test_balance_operations_balance_zero(self):
        client = Client()
        client.force_login(self.user)
        balance_operations_url = reverse('operations')
        response = client.get(balance_operations_url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'You have a zero balance')