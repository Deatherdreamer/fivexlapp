from django.contrib import admin

# Register your models here.
from .models import *

admin.site.register(Profile)
admin.site.register(Earnings)
admin.site.register(Deposits)
admin.site.register(Withdrawals)
admin.site.register(Investments)
admin.site.register(Tasks_Test)
admin.site.register(FrequentlyAskedQuestions)
admin.site.register(WithdrawalPeriods)







