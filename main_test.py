import unittest
from unittest.mock import patch
from main import statement


class StatementTests(unittest.TestCase):
    def setUp(self):
        self.roles = {
            'dev': {'experience': 'junior'},
            'lead': {'experience': 'senior'}
        }

    def test_junior_no_discount(self):
        invoice = {
            'customer': 'Acme Corp',
            'team': [{'role': 'dev', 'days': 10}]
        }

        result = statement(invoice, self.roles)

        self.assertIn("dev: $5,000.00 (10 days)", result)
        self.assertIn("Amount owed is $5,000.00", result)
        self.assertIn("You receive a volume discount: $0.00", result)

    def test_junior_with_discount(self):
        invoice = {
            'customer': 'Beta Inc',
            'team': [{'role': 'dev', 'days': 45}]
        }

        result = statement(invoice, self.roles)

        # 500 * 45 - 0.2 * (45 - 20) * 500 = 22500 - 2500 = 20000
        self.assertIn("dev: $20,000.00 (45 days)", result)
        self.assertIn("Amount owed is $20,000.00", result)
        # Volume: floor(45/40)*500 = 500, + floor(45/20)*500 = 1000 => 1500
        self.assertIn("You receive a volume discount: $1,500.00", result)

    def test_senior_with_discount(self):
        invoice = {
            'customer': 'Gamma LLC',
            'team': [{'role': 'lead', 'days': 50}]
        }

        result = statement(invoice, self.roles)

        # 1000 * 50 - 0.1 * (50 - 20) * 1000 = 50000 - 3000 = 47000
        self.assertIn("lead: $47,000.00 (50 days)", result)
        self.assertIn("Amount owed is $47,000.00", result)
        # Volume discount: floor(50/40)*500 = 500
        self.assertIn("You receive a volume discount: $500.00", result)

    def test_invalid_experience_level(self):
        roles = {'dev': {'experience': 'intern'}}
        invoice = {
            'customer': 'Delta Co',
            'team': [{'role': 'dev', 'days': 10}]
        }

        with self.assertRaises(ValueError) as context:
            statement(invoice, roles)

        self.assertIn("Unknown experience level", str(context.exception))


if __name__ == '__main__':
    unittest.main()
