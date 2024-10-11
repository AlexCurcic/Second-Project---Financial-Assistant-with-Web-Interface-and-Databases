from django.test import TestCase
from unittest.mock import patch
from ..views import *

class CurrencyParamsTestCase(TestCase):
    @patch('requests.get')
    def test_get_currency_params_success(self, mock_get):
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = {
            'AUD': 1.62,
            'CAD': 1.48,
            'CHF': 1.08,
            'EUR': 1.0,
            'GBP': 0.88,
            'JPY': 129.5,
            'USD': 1.15
        }


        data, currency_choices = getCurrencyParams()

        self.assertIsNotNone(data)
        self.assertIsNotNone(currency_choices)
        self.assertIsInstance(data, dict)
        self.assertIsInstance(currency_choices, list)
        self.assertEqual(len(currency_choices), 7)

        expected_currency_choices = [
            ('AUD', 'AUD (1.62)'), ('CAD', 'CAD (1.48)'), ('CHF', 'CHF (1.08)'),
            ('EUR', 'EUR (1.0)'), ('GBP', 'GBP (0.88)'), ('JPY', 'JPY (129.5)'),
            ('USD', 'USD (1.15)')
        ]
        self.assertEqual(currency_choices, expected_currency_choices)