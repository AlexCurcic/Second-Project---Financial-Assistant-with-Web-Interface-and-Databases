from django.test import TestCase
from django.template.loader import render_to_string
from ..views import *

class CurrencyExchangeTemplateTestCase(TestCase):
    def test_currency_choices_rendering(self):
        currency_choices = [('USD', 'USD (1.0)'), ('EUR', 'EUR (0.85)'), ('GBP', 'GBP (0.72)')]
        context = {'currency_choices': currency_choices}

        rendered = render_to_string('app/currency_exchange.html', context)

        for currency, label in currency_choices:
            self.assertInHTML(f'<option value="{currency}">{label}</option>', rendered)

    def test_transaction_details_rendering(self):
        context = {'amount': 100, 'currency': 'EUR', 'exchanged_amount': 85}

        rendered = render_to_string('app/currency_exchange.html', context)

        self.assertInHTML('<p><strong>Amount:</strong> 100</p>', rendered)
        self.assertInHTML('<p><strong>Currency:</strong> EUR</p>', rendered)
        self.assertInHTML('<p><strong>Exchanged Amount:</strong> 85</p>', rendered)