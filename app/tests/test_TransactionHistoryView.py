from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse
from ..models import History  
from ..views import *

class ViewTransactionHistoryViewTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.history_url = reverse('history')

    def test_transaction_history_view_login_required(self):
        response = self.client.get(self.history_url)
        self.assertEqual(response.status_code, 302) 

        user = User.objects.create_user(username='testuser', password='testpassword')
        self.client.force_login(user)
        response = self.client.get(self.history_url)
        self.assertEqual(response.status_code, 200)

    def test_transaction_history_view_context(self):
        user = User.objects.create_user(username='testuser', password='testpassword')
        self.client.force_login(user)
        response = self.client.get(self.history_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'app/history.html')
        self.assertIn('transactions', response.context)
        self.assertEqual(len(response.context['transactions']), 0)

        History.objects.create(user=user, amount=100, type='deposit', status='success')
        History.objects.create(user=user, amount=50, type='withdraw', status='success')

        response = self.client.get(self.history_url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['transactions']), 2) 

    def test_transaction_history_view_only_user_transactions(self):
        user1 = User.objects.create_user(username='testuser1', password='testpassword1')
        user2 = User.objects.create_user(username='testuser2', password='testpassword2')
        self.client.force_login(user1)

        History.objects.create(user=user1, amount=100, type='deposit', status='success')
        History.objects.create(user=user2, amount=50, type='withdraw', status='success')

        response = self.client.get(self.history_url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['transactions']), 1) 