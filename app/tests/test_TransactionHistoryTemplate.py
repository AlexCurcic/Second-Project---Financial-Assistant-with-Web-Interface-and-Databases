from django.test import TestCase
from django.contrib.auth.models import User
from django.template.loader import render_to_string
from ..models import History  
from ..views import *




class TransactionHistoryTemplateTestCase(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        History.objects.create(user=self.user, status='success', amount=100)
        History.objects.create(user=self.user, status='failure', amount=50)
        History.objects.create(user=self.user, status='success', amount=75)


    def test_transaction_history_rendering(self):
        transactions = History.objects.all()
        context = {'transactions': transactions}
        rendered = render_to_string('app/history.html', context)

        for transaction in transactions:
            self.assertInHTML(f'Date: {transaction.datetime.strftime("%d/%m/%Y %H:%M:%S")}', rendered)
            self.assertInHTML(f'Status: {transaction.status}', rendered)
            self.assertInHTML(f'Balance After: {transaction.amount}', rendered)

    def test_empty_transaction_history_rendering(self):
        context = {'transactions': []}
        rendered = render_to_string('app/history.html', context)
        self.assertInHTML('<li class="list-group-item">No transactions found.</li>', rendered)
