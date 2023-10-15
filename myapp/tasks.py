from celery import shared_task
from myapp.models import *
import time

@shared_task
def generate_returns_for_all_investments():
    investments = Investments.objects.all()
    for investment in investments:
        investment.generate_returns()

@shared_task
def check_status_of_all_deposits():
    deposits = Deposits.objects.filter(status='pending')
    for deposit in deposits:
        try:
            deposit.check_status()
        except:
            print('Error checking status of deposit: ' + str(deposit.id))

@shared_task
def test_celery():
    print('Starting test_celery task...')
    Tasks_Test.objects.create(name="Test Celery Task")
    print('test_celery task complete!')