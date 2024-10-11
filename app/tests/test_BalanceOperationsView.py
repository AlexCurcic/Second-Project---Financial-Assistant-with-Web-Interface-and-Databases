from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse
from ..models import History  
from ..views import *

class BalanceOperationsViewTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.operations_url = reverse('operations') 

    def test_balance_operations_view_get(self):
        user = User.objects.create_user(username='testuser', password='testpassword')
        self.client.force_login(user)
        response = self.client.get(self.operations_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'app/operations.html')
        self.assertIn('balance', response.context)
        self.assertEqual(response.context['username'], 'testuser')

    def test_balance_operations_view_post_deposit(self):
        user = User.objects.create_user(username='testuser', password='testpassword')
        self.client.force_login(user)
        data = {
            'amount': '100',
            'operation': 'deposit',
        }
        response = self.client.post(self.operations_url, data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(History.objects.filter(user=user).count(), 1)
        self.assertEqual(History.objects.filter(user=user, status='success').count(), 1)

    def test_balance_operations_view_post_withdraw_success(self):
        user = User.objects.create_user(username='testuser', password='testpassword')
        History.objects.create(user=user, amount=100, type='deposit', status='success')
        self.client.force_login(user)
        data = {
            'amount': '50',
            'operation': 'withdraw',
        }
        response = self.client.post(self.operations_url, data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(History.objects.filter(user=user).count(), 2)
        self.assertEqual(History.objects.filter(user=user, status='success').count(), 2)

    def test_balance_operations_view_post_withdraw_failure(self):
        user = User.objects.create_user(username='testuser', password='testpassword')
        History.objects.create(user=user, amount=100, type='deposit', status='success')
        self.client.force_login(user)
        data = {
            'amount': '150',
            'operation': 'withdraw',
        }
        response = self.client.post(self.operations_url, data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(History.objects.filter(user=user, status='failure').count(), 1)

    def test_balance_operations_view_login_required(self):
        response = self.client.get(self.operations_url)
        self.assertEqual(response.status_code, 302)  

        user = User.objects.create_user(username='testuser', password='testpassword')
        self.client.force_login(user)
        response = self.client.get(self.operations_url)
        self.assertEqual(response.status_code, 200)  