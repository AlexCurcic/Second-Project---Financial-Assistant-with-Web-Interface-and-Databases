from django.test import TestCase
from django.contrib.auth.models import User
from ..models import History  
from ..views import *

class BalanceCalculationTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create(username='testuser')

    def test_get_balance_empty_history(self):
        balance = getBalance(self.user)
        self.assertEqual(balance, 0.0)

    def test_get_balance_with_transactions(self):
        History.objects.create(user=self.user, amount=100, type='deposit', status='success')
        History.objects.create(user=self.user, amount=50, type='withdraw', status='success')
        History.objects.create(user=self.user, amount=25, type='deposit', status='success')
        expected_balance = 100 + 25 - 50
        balance = getBalance(self.user)
        
        self.assertEqual(balance, expected_balance)