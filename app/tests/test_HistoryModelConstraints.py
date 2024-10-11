from django.test import TestCase
from django.contrib.auth.models import User
from django.db.utils import IntegrityError
from ..models import History  
from ..views import *




class HistoryModelConstraintsTestCase(TestCase):

    def setUp(self):
        self.user = User.objects.create(username='testuser', password='testpassword')

    def test_max_digits_amount(self):
        with self.assertRaises(Exception):
            History.objects.create(
                status='success',
                amount=100000000000,
                type='deposit',
                user=self.user
            )
    def test_foreign_key_user(self):
        with self.assertRaises(IntegrityError):
            History.objects.create(
                status='success',
                amount=100.00,
                type='deposit'
            )
