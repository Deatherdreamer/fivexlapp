from django.db import models
from django.contrib.auth.models import User
from django.db.models import Sum
from datetime import datetime, timedelta
from decimal import Decimal
from django.conf import settings
import requests
import random
import string


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    firstName = models.CharField(max_length=100, default='')
    lastName = models.CharField(max_length=100, default='')
    phone = models.CharField(max_length=100, default='')
    country = models.CharField(max_length=100, default='')
    dateOfBirth = models.DateField(null=True, blank=True)
    dateJoined = models.DateField(auto_now_add=True)
    referral_code = models.CharField(max_length=12, unique=True, blank=True)
    referred_by = models.ForeignKey(
        'self', on_delete=models.SET_NULL, null=True, blank=True)

    balance = models.DecimalField(max_digits=20, decimal_places=2, default=0, blank=True)
    ewallet = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return f'{self.firstName} {self.lastName}'

    def save(self, *args, **kwargs):
        if not self.referral_code:
            self.referral_code = self.generate_referral_code()
        super().save(*args, **kwargs)

    def get_full_name(self):
        return f"{self.firstName} {self.lastName}"

    def get_short_name(self):
        return self.firstName[0] + ". " + self.lastName

    def getReferredUsers(self, level=3, tier=1):
        if level == 0:
            return []
        referred_users = list(Profile.objects.filter(referred_by=self))
        for referred_user in referred_users:
            referred_user.tier = tier
            referred_user.referred_users = referred_user.getReferredUsers(
                level=level-1, tier=tier+1)
        all_referred_users = referred_users.copy()
        for referred_user in referred_users:
            all_referred_users += referred_user.getReferredUsers(
                level=level-1, tier=tier+1)
        return all_referred_users

    def generate_referral_code(self):
        letters = string.ascii_uppercase + string.digits
        code = ''.join(random.choice(letters) for i in range(12))
        while Profile.objects.filter(referral_code=code).exists():
            code = ''.join(random.choice(letters) for i in range(12))
        return code

    def getReferredUsersCount(self):
        return Profile.objects.filter(referred_by=self).count()

    def getCountOfDeposits(self):
        return Deposits.objects.filter(user=self.user).count()
    
    def getCountOfDepositsCompleted(self):
        return Deposits.objects.filter(user=self.user, status='completed').count()
    
    def getCountOfDepositsPending(self):
        return Deposits.objects.filter(user=self.user, status__in=['pending', 'created']).count()
    
    def getCountOfDepositsCancelled(self):
        return Deposits.objects.filter(user=self.user, status='cancelled').count()

    def getTotalDeposits(self):
        total = 0
        for deposit in Deposits.objects.filter(user=self.user, status='completed'):
            total += deposit.amount
        return total
    

    def getCountOfInvestments(self):
        return Investments.objects.filter(user=self.user).count()

    def getTotalInvestments(self):
        total = 0
        for investment in Investments.objects.filter(user=self.user):
            total += investment.amount
        return total
    
    def getCountOfInvestmentsCompleted(self):
        return Investments.objects.filter(user=self.user, percentage_returned=200).count()
    
    def getCountOfInvestmentsPending(self):
        return Investments.objects.filter(user=self.user, percentage_returned__lt=200).count()

    def getEarningsByInvestment(self):    
        investments = Investments.objects.filter(user=self.user)
        total = 0
        for investment in investments:
            total += investment.returns
        return total
           
    

    def getTotalEarnings(self):
        total = 0
        for earnings in Earnings.objects.filter(user=self.user):
            total += earnings.amount
        return total
    
    def getTotalEarningsByReferrals(self):
        total = 0
        earnings = Earnings.objects.filter(user=self.user).exclude(investment__in=Investments.objects.filter(user=self.user))
        for earning in earnings:
            total += earning.amount
        return total
    
    def getTotalEarningsByInvestments(self):
        total = 0
        earnings = Earnings.objects.filter(user=self.user, investment__in=Investments.objects.filter(user=self.user))
        for earning in earnings:
            total += earning.amount
        return total
        

    def getCurrentBalance(self):
        deposits = Deposits.objects.filter(user=self.user, status='completed')
        investments = Investments.objects.filter(user=self.user)
        withdrawals = Withdrawals.objects.filter(user=self.user)
        earnings = Earnings.objects.filter(user=self.user)
        deposit_total = deposits.aggregate(
            Sum('amount'))['amount__sum'] or 0
        investment_total = investments.aggregate(
            Sum('amount'))['amount__sum'] or 0
        withdrawal_total = withdrawals.aggregate(
            Sum('amount'))['amount__sum'] or 0
        earnings_total = earnings.aggregate(
            Sum('amount'))['amount__sum'] or 0
        
        return deposit_total + earnings_total - withdrawal_total - investment_total     


class Deposits(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=20, decimal_places=2)
    currency = models.CharField(max_length=10)    
    date = models.DateField(auto_now_add=True)
    charge_id = models.CharField(max_length=100, default='')
    status = models.CharField(max_length=100, default='created')


    def __str__(self):
        return f'{self.user.username} - {self.amount} {self.currency}'

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        profile = self.user.profile
        profile.balance = profile.getCurrentBalance()
        profile.save()

    def check_status(self):
        url = f'https://api.kodexpay.com/api/v1/payment/status/{self.charge_id}'
        response = requests.get(url, headers={'API-TOKEN': settings.KODEXPAY_API_KEY})        
        data = response.json()
        if data['statusId'] == '4':
            self.status = 'completed'
            self.save()
            print('Deposit completed successfully.')
        elif data['statusId'] == '3':
            self.status = 'cancelled'
            self.save()
            print('Deposit cancelled.')
        elif data['statusId'] == '2':
            self.status = 'pending'
            self.save()
            print('Deposit failed.')        
        else:
            self.status = 'created'
            self.save()
            print('Deposit not completed yet.')  
       

class Withdrawals(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=20, decimal_places=2)
    currency = models.CharField(max_length=10, default='USDT')
    aprroved = models.BooleanField(default=False)
    date = models.DateField(auto_now_add=True)

    def __str__(self):
        return f'{self.user.username} - {self.amount}'
    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        profile = self.user.profile
        profile.balance = profile.getCurrentBalance()
        profile.save()



class Investments(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=20, decimal_places=2)
    returns = models.DecimalField(max_digits=20, decimal_places=2, default=0)
    percentage_returned = models.IntegerField(default=0, editable=False, blank=True, null=True)
    # date = models.DateTimeField(default=datetime.now, blank=True, editable=False)
    date = models.DateTimeField(auto_now_add=True)
    last_updated = models.DateTimeField(auto_now=True, null=True, blank=True)


    def __str__(self):
        return f'{self.user.username} - {self.amount} - {self.date}'
        

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        profile = self.user.profile
        profile.balance = profile.getCurrentBalance()
        profile.save()

    def calculate_returns(self):
        self.percentage_returned = round((self.returns / self.amount) * 100, 2)

    def generate_returns(self):        
        now = datetime.now()        
        them = datetime(self.last_updated.year, self.last_updated.month, self.last_updated.day, self.last_updated.hour, self.last_updated.minute, self.last_updated.second)
        if now - them > timedelta(hours=24) and self.percentage_returned <= 200:
            print('Investment matured. Generating returns...')
            self.returns += self.amount * Decimal('0.01')
            #calculate percentage returned
            self.calculate_returns()
            self.save()
            Earnings.objects.create(investment=self, amount=self.amount * Decimal('0.01'), user=self.user, description='Daily Returns of 1% of Investment.')    
        else:
            print('Investment not matured yet.')
   
      
class Earnings(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    investment = models.ForeignKey(Investments, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=20, decimal_places=2)
    description = models.CharField(max_length=100, default='')
    date = models.DateField(auto_now_add=True)
    

    def __str__(self):
        return f'{self.user.username} - {self.amount}'
    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        profile = self.user.profile
        profile.balance = profile.getCurrentBalance()
        profile.save()
    
class Tasks_Test(models.Model):
    name = models.CharField(max_length=100, default='')
    date = models.DateField(auto_now_add=True)

    def __str__(self):
        return f'{self.date} - {self.name}'
    
class FrequentlyAskedQuestions(models.Model):
    question = models.CharField(max_length=100, default='')
    answer = models.TextField(default='')

    def __str__(self):
        return f'{self.question}'
    
class WithdrawalPeriods(models.Model):
    withdrawal_authorization = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.withdrawal_authorization}'
    
    