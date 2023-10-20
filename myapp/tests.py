from django.test import TestCase
from myapp.models import *

class DepositsModelTest(TestCase):
    def setUp(self):
        # Create a user and profile for testing
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.profile = Profile.objects.create(user=self.user, balance=0.00)

    def test_deposit_creation(self):
        # Create a deposit for testing
        deposit = Deposits.objects.create(user=self.user, amount=50.00, currency='USD', charge_id='ch_1234')

        # Check if the deposit was created successfully
        self.assertEqual(deposit.user, self.user)
        self.assertEqual(deposit.amount, 50.00)
        self.assertEqual(deposit.currency, 'USD')
        self.assertEqual(deposit.charge_id, 'ch_1234')
        self.assertEqual(deposit.status, 'created')

        deposit.status = 'completed'
        deposit.save()

        # Check if the deposit status was updated correctly


        # Check if the profile balance was updated correctly
        self.assertEqual(self.profile.balance, 50.00)


class ProfileModelTest(TestCase):
    def setUp(self):
        # Create a user and profile for testing
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.profile = Profile.objects.create(user=self.user, balance=0.00)

    def test_profile_creation(self):
        # Check if the profile was created successfully
        self.assertEqual(self.profile.user, self.user)
        self.assertEqual(self.profile.balance, 0.00)
    
    def test_profile_balance_update(self):
        # Update the profile balance
        self.profile.balance = 100.00
        self.profile.save()

        # Check if the profile balance was updated correctly
        self.assertEqual(self.profile.balance, 100.00)

class InvestmentsModelTest(TestCase):
    def setUp(self):
        # Create a user and profile for testing
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.profile = Profile.objects.create(user=self.user, balance=50.00)

    def test_investment_creation(self):
        # Create an investment for testing
        investment = Investments.objects.create(user=self.user, amount=50.00)

        # Check if the investment was created successfully
        self.assertEqual(investment.user, self.user)
        self.assertEqual(investment.amount, 50.00)

    def test_investment_status_update(self):
        # Create an investment for testing
        investment = Investments.objects.create(user=self.user, amount=50.00)

        # Update the investment status
        investment.status = 'completed'
        investment.save()

        # Check if the investment status was updated correctly
        self.assertEqual(investment.status, 'completed')

    def test_profile_balance_update(self):
        # Create an investment for testing
        investment = Investments.objects.create(user=self.user, amount=50.00)

        # Check if the profile balance was updated correctly
        self.assertEqual(self.profile.balance, -50.00)


