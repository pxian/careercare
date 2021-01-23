from .models import Employer
from django.test import TestCase
from django.contrib.auth.models import User


class SettingsTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='test', password='12345')
        self.user.save()
        self.account = Employer.objects.create(
            user_id=self.user.id,
            name='Zimi Tech Inc.',
            industry='Accounting'
        )
        self.account.save()

    def test_read_account(self):
        self.assertEqual(self.account.user_id, self.user.id)
        self.assertEqual(self.account.name, 'Zimi Tech Inc.')
        self.assertEqual(self.account.industry, 'Accounting')

    def test_update_account(self):
        self.account.name = 'Harry Quarry'
        self.account.save()
        self.assertEqual(self.account.name, 'Harry Quarry')
        self.account.industry = 'Computer/IT'
        self.account.save()
        self.assertEqual(self.account.industry, 'Computer/IT')

    def test_delete_account(self):
        self.user.delete()
