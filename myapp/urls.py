from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('login/', views.loginUser, name='login'),
    path('logout/', views.logoutUser, name='logout'),
    path('register/', views.register, name='register'),
    path('register/<str:referralCode>', views.register, name='register'),
    path('profile/', views.profile, name='profile'),
    path('profile/update', views.editProfile, name='updateProfile'),
    path('referrals/', views.referrals, name='referrals'),
    path('deposits/', views.deposits, name='deposits'),
    path('deposits/new', views.newDeposit, name='newDeposit'),
    path('paydeposit/<int:deposit_id>', views.payDeposit, name='payment'),
    path('withdrawals/', views.withdrawals, name='withdrawals'),
    path('withdrawals/new', views.newWithdrawal, name='newWithdrawal'),
    path('investments/', views.investments, name='investments'),
    path('investments/new', views.newInvestment, name='newInvestment'),    
    path('earnings/', views.earnings, name='earnings'),
    path('generate/', views.generate, name='generateEarnings'),
    path('test-celery/', views.test_celery_view, name='test_celery'),
    path('frequentlyaskedquestions/', views.frequentlyAskedQuestions, name='faqs'), 
    path('401/', views.unauthorized, name='unauthorized'),  




    
]
