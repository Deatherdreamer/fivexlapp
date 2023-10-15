from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db import transaction
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from .models import *
from .forms import *
from django.contrib import messages
from decimal import Decimal
import logging

from bigdatave import settings

from .tasks import *
import requests

# def pay(request):
#     pass
    
    
# def pay_status(request):
#     url = 'https://api.kodexpay.com/api/v1/payment/status/66d876f8-52c4-42df-9f1e-536dad5c918c'
#     response = requests.get(url, headers={'API-TOKEN': settings.KODEXPAY_API_KEY})
#     print(response.json())
#     if response.status_code == 200:
#         return HttpResponse(response.json())
#     elif response.status_code == 400:
#         return HttpResponse(response.json())
#     else:
#         return HttpResponse(response.json())


def loginUser(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect("index")
        else:
            messages.error(request, "Invalid credentials")
            return render(request, "login.html")
    else:
        return render(request, "login.html")


@login_required
def logoutUser(request):
    logout(request)
    return redirect("index")


@login_required
def index(request):
    profile = Profile.objects.get(user=request.user)
    return render(request, "index.html", {"profile": profile})


# register
def register(request, referralCode=None):
    if request.method == "POST":
        firstName = request.POST.get("firstName")
        lastName = request.POST.get("lastName")
        country = request.POST.get("country")
        phone = request.POST.get("phone")
        dateOfBirth = request.POST.get("dateOfBirth")
        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password")
        cpassword = request.POST.get("cpassword")
        referralCode = request.POST.get("referralCode") or referralCode


        if password == cpassword:
            if User.objects.filter(username=username).exists():
                messages.error(request, "Username already exists")
                return redirect("register", referralCode=referralCode)
            elif User.objects.filter(email=email).exists():
                messages.error(request, "Email already exists")
                return redirect("register", referralCode=referralCode)
            else:
                with transaction.atomic():
                    user = User.objects.create_user(
                        username=username, email=email, password=password
                    )
                    user.save()
                    referred_by = None
                    if referralCode:
                        referred_by = Profile.objects.filter(
                            referral_code=referralCode
                        ).first()
                        if not referred_by:
                            messages.error(request, "Invalid referral code")
                            return redirect("register")
                    if referred_by:
                        profile = Profile.objects.create(
                            user=user,
                            firstName=firstName,
                            lastName=lastName,
                            phone=phone,
                            country=country,
                            dateOfBirth=dateOfBirth,
                            referred_by=referred_by,
                            
                        )
                        profile.save()
                        messages.success(
                            request, "Account created successfully")
                        return redirect("login")
                    else:
                        profile = Profile.objects.create(
                            user=user,
                            firstName=firstName,
                            lastName=lastName,
                            phone=phone,
                            country=country,
                            dateOfBirth=dateOfBirth
                        )
                        profile.save()
                        messages.success(
                            request, "Account created successfully")
                        return redirect("login")
        else:
            messages.error(request, "Password does not match")
            return redirect("register", referralCode=referralCode)
    else:
        context = {}
        if referralCode:
            referred_by = Profile.objects.filter(
                referral_code=referralCode).first()
            if not referred_by:
                messages.error(request, "Invalid referral code")
            else:
                context["referralCode"] = referralCode
        return render(request, "register.html", context)

# view to display profile
@login_required
def profile(request):
    profile = Profile.objects.get(user=request.user)
    return render(request, "profile.html", {"profile": profile})

# view to display edit profile
@login_required
def editProfile(request):
    profile = Profile.objects.get(user=request.user)
    if request.method == "POST":
        form = ProfileForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, "Profile updated successfully")
            return redirect("profile")
        else:
            print(form.errors)
            messages.error(request, "Invalid form")
            return redirect("updateProfile")
    else:
        form = ProfileForm(request.POST, instance=profile)
        return render(request, "editProfile.html", {"profile": profile, "form": form})



# view to display referrals
@login_required
def referrals(request):
    referrals = request.user.profile.getReferredUsers()
    referrals = sorted(
        referrals, key=lambda referred_user: referred_user.tier, reverse=False
    )
    return render(request, "referrals.html", {"referrals": referrals})


@login_required
def deposits(request):
    deposits = request.user.deposits_set.all().order_by("date")

    return render(request, "deposits.html", {"deposits": deposits})


@login_required
def newDeposit(request):
    if request.method == "POST":
        #create a new transaction in kodexpay
        amount = float(request.POST.get("amount"))
        
        if (amount and amount > 0):
            deposit = Deposits.objects.create(
            user=request.user, amount=amount, currency="USDT"
            )        
            url = 'https://api.kodexpay.com/api/v1/payment'
            data = {
                    'token':'usdtt',
                    'quantity':amount,
                    'paymentToken': 'usdtt',
                    'purchaseEmail' : request.user.email,
                    'purchaseName': request.user.username,
                    'invoiceNumber': deposit.id,
                }
            response = requests.post(url, headers={'API-TOKEN': settings.KODEXPAY_API_KEY}, json=data)
            deposit.charge_id = response.json()['transactionId']
            deposit.save()
            messages.error(request, "Transaction created successfully, please go to details to pay")
            return redirect("deposits")  
        else:
            messages.error(request, "Invalid amount")
            return redirect("newDeposit") 
             
    else:
        return render(request, "newDeposit.html")
    
@login_required
def payDeposit(request, deposit_id):
    deposit = Deposits.objects.get(id=deposit_id)
    url = f'https://api.kodexpay.com/api/v1/payment/status/{deposit.charge_id}'
    response = requests.get(url, headers={'API-TOKEN': settings.KODEXPAY_API_KEY})
    return render(request, "payment.html", {"response": response.json()})


# @login_required
# def depositSuccess(request):
#     charge_id = request.session["charge_id"]
#     amount = float(request.session["amount"])
#     # Save the deposit to the database
#     deposit = Deposits.objects.create(
#         user=request.user, amount=amount, currency="USDT", charge_id=charge_id
#     )
#     deposit.save()
#     request.session["amount"] = None
#     request.session["charge_id"] = None    

#     messages.error(request, "Deposit Successful")
#     return redirect("deposits")


# @login_required
# def depositFailed(request):
#     request.session["amount"] = None
#     request.session["currency"] = None
#     request.session["charge_id"] = None
#     messages.error(request, "Deposit Cancelled")
#     return redirect("deposits")


@login_required
def investments(request):
    investments = request.user.investments_set.all().order_by("-date")
    return render(request, "investments.html", {"investments": investments})


@login_required
def newInvestment(request):
    availableBalance = request.user.profile.balance
    if request.method == "POST":
        amount = request.POST.get("amount")
        if (amount and float(amount) > availableBalance):
            messages.error(request, "Insufficient balance")
            return redirect("newInvestment")
        elif (amount and float(amount) <= 0):
            messages.error(request, "Invalid amount")
            return redirect("newInvestment")
        elif amount:
            amount = float(amount)
            with transaction.atomic():
                investment = Investments.objects.create(
                    user=request.user, amount=amount
                )
                investment.save()
                referrer = request.user.profile.referred_by
                if referrer:
                    referrerEarnings = Earnings.objects.create(
                        investment=investment,
                        user=referrer.user,
                        amount=amount * 0.03,
                        description=f"{request.user.profile} Invested {amount}. You earned 3%.",
                    )
                    referrerEarnings.save()

                    grandReferrer = referrer.referred_by
                    if grandReferrer:
                        grandReferrerEarnings = Earnings.objects.create(
                            investment=investment,
                            user=grandReferrer.user,
                            amount=amount * 0.02,
                            description=f"{request.user.profile} Invested {amount}. You earned 2%.",
                        )
                        grandReferrerEarnings.save()

                        greatGrandReferrer = grandReferrer.referred_by
                        if greatGrandReferrer:
                            greatGrandReferrerEarnings = Earnings.objects.create(
                                investment=investment,
                                user=greatGrandReferrer.user,
                                amount=amount * 0.01,
                                description=f"{request.user.profile} Invested {amount}. You earned 1%.",
                            )
                            greatGrandReferrerEarnings.save()

            messages.success(request, "Investment successful")
            return redirect("investments")
        else:
            messages.error(request, "Invalid amount")
            return redirect("newInvestment")
    else:
        return render(request, "newInvestment.html")


@login_required
def earnings(request):
    earnings = request.user.earnings_set.all().order_by("-investment__date")
    return render(request, "earnings.html", {"earnings": earnings})

@login_required
def generate(request):
    investments = Investments.objects.all()
    for investment in investments:
        investment.generate_returns()
    return render(request, "generate.html", {"investments": investments})
    
    # messages.success(request, "Returns generated successfully")
    # return redirect("earnings")


def test_celery_view(request):
    test_celery.delay()
    return HttpResponse('Celery task started!')

def frequentlyAskedQuestions(request):
    faqs = FrequentlyAskedQuestions.objects.all()
    return render(request, "FAQ.html", {"faqs": faqs})

def withdrawals(request):
    withdrawals = request.user.withdrawals_set.all().order_by("-date")
    return render(request, "withdrawals.html", {"withdrawals": withdrawals})

@login_required
def newWithdrawal(request):
    period_is_active = WithdrawalPeriods.objects.first()
    if not period_is_active.withdrawal_authorization:
        messages.error(request, "Withdrawal period is not active")
        return redirect("unauthorized")
    else:
        if request.method == "POST":
            amount = float(request.POST.get("amount"))
            if amount > request.user.profile.balance:
                messages.error(request, "Insufficient balance")
                return redirect("newWithdrawal")
            else:
                withdrawal = Withdrawals.objects.create(
                    user=request.user, amount=amount
                )
                withdrawal.save()
                messages.success(request, "Withdrawal successful")
                return redirect("withdrawals")
        return render(request, "newWithdrawal.html")

        
        
        
def unauthorized(request):
    return render(request, "401.html")