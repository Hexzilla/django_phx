from django.shortcuts import render , redirect
from django.http import HttpResponse,JsonResponse
from django.forms import inlineformset_factory
from django.contrib import messages
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import UserCreationForm
# from django.contrib.sessions.models import Session
from django.utils import timezone
from django.http import HttpResponseRedirect
from django.template.loader import render_to_string
from django.core.paginator import Paginator
from django.db.models import Q, F, Sum, Count
from django.db.models.functions import Replace
from django.contrib.auth.models import User

import dateutil.parser
from datetime import datetime, date, timedelta, time
from itertools import chain
from django.contrib.auth.decorators import login_required
# from django.contrib.auth.models import Group

from .decorators import unauthenticated_user, allowed_users, admin_only
from .filters import *	#all filters
from .forms import * 	#all forms
from .models import * 	#all models

import logging
logger = logging.getLogger(__name__)


# Create your views here.
#!login system3

def activeDate_on_all_page(request): # show activate dated
	# import socket

	hostname 		  = request.get_host()
	timeNow_side      = datetime.now().date()
	present           = datetime.now()
	future            = datetime(2020, 9, 24)
	active_date		  = datetime.now() - datetime(2020, 9, 24)
	active_date1	  = datetime.now() - datetime(2020, 12, 10)
	active_date2	  = datetime.now() - datetime(2020, 9, 24)
	active_date3	  = datetime.now() - datetime(2020, 9, 24)
	
	return {'active_date': active_date,
	'active_date1': active_date1,
	'active_date2': active_date2,
	'active_date3': active_date3,
	'timeNow_side':timeNow_side,"hostname":hostname}

# @unauthenticated_user
def loginPage(request):
	today_now = timezone.datetime.now().strftime("%Y%m%d")
	# today_now = timezone.datetime.now().strptime("%d-%m-%Y")
	
	if request.method == 'POST':
		username = request.POST.get('username')
		password = request.POST.get('password')
		user = authenticate(request, username=username, password=password)

		if user is not None:
			login(request, user)
			return redirect('home')
			
		# if int(today_now) > int(LoginAccess()):
		# 	messages.info(request, 'Username OR password is incorrect')
		# elif user is not None:
		# 	login(request, user)
		# 	return redirect('home')
		# else:
		# 	messages.info(request, 'Username OR password is incorrect')

	context = {}
	return render(request, 'accounts/login/login.html', context)


def logoutUser(request):
	logout(request)
	return redirect('login')

#* login end





#! Main Dashboard

# login needed	=====================
# @admin_only
@login_required(login_url='login')
def home(request):
	

	deposits          = Transaction.objects.filter(Q(tag="Deposit") | Q(tag="Free")| Q(tag="Recommend")| Q(tag="Lock")| Q(tag="Borrow")).filter(completed="No").order_by("-id")
	withdrawals       = Transaction.objects.filter(tag="Withdrawal").filter(completed="No").order_by("-id")
	transfers         = Transaction.objects.filter(tag="Transfer").filter(completed="No").order_by("-id")
	successMessage    = SuccessMessage.objects.all().last()
	bank              = Bank.objects.all().order_by("id")
	form              = WithdrawalBankForm()
	timeNow           = timezone.now()
	present           = datetime.now()
	
	context = {
		'successMessage':successMessage,'deposits' : deposits, 'withdrawals' : withdrawals, 'transfers' : transfers, 'bank':bank , 'form':form ,
	}
	return render(request, 'accounts/main/dashboard.html', context)



@login_required(login_url='login')
def refresh_dashboard(request):	#refresh Dashboard
	data = dict()
	if request.method == "GET":
		deposits        = Transaction.objects.filter(Q(tag="Deposit") | Q(tag="Free")| Q(tag="Recommend")| Q(tag="Lock")| Q(tag="Borrow")).filter(completed="No")
		withdrawals     = Transaction.objects.filter(tag="Withdrawal").filter(completed="No")
		transfers       = Transaction.objects.filter(tag="Transfer").filter(completed="No")
		successMessage  = SuccessMessage.objects.all().last()

	context =	{'deposits': deposits, 'withdrawals': withdrawals, 'transfers': transfers, 'successMessage': successMessage}
	# return render(request, 'accounts/dashboard.html', context)
	data['html_table'] = render_to_string('accounts/main/dashboard_action.html',context,request = request)
	return JsonResponse(data)


#* dashboard end




#!	user_customer

# @allowed_users(allowed_roles=['admin'])
@login_required(login_url='login')
def user_profile(request,pk):
	games			= Game.objects.all().order_by("id")
	customer		= Customer.objects.get(id=pk)
	customergames	= CustomerGame.objects.filter(customerID=pk)
	transation      = Transaction.objects.filter(customer=pk).order_by('-id')
	timeNow         = timezone.now()
	timeNow_date	= timeNow.date()
	# promotion1	= weeklyPromotion(request)
	promotion1, promotion1_start_week, promotion1_end_week, promotion1_prv_start_week = weeklyPromotion(request)
	if timeNow_date == promotion1_start_week:
		weeklyTransactionNow  = transation.filter(tag="Deposit").filter(status="Approved").filter(completed="Yes").filter(action_approve__gt = promotion1_prv_start_week, action_approve__lt = promotion1_start_week).aggregate(Sum('amount'))
	else:
		weeklyTransactionNow  = transation.filter(tag="Deposit").filter(status="Approved").filter(completed="Yes").filter(action_approve__gt = promotion1_start_week, action_approve__lt = promotion1_end_week).aggregate(Sum('amount'))
	if weeklyTransactionNow["amount__sum"] is None:
		weeklyTransactionNow = 0
	else:
		weeklyTransactionNow = weeklyTransactionNow["amount__sum"]
	if promotion1 is not None:
		promotionPrecentage   =	(weeklyTransactionNow * promotion1.amount_percentage) /100
		if promotionPrecentage > 500:
			promotionPrecentage = 500
		promo_min_withdrawal = promotionPrecentage * promotion1.min_withdrawal_turnover
		promo_max_withdrawal = promotionPrecentage * promotion1.max_withdrawal_turnover
	else:
		promotionPrecentage = 0
		promo_min_withdrawal = 0
		promo_max_withdrawal = 0

	context 	= {'customer' : customer, 'customergames':customergames,'promotion1':promotion1, 'weeklyTransactionNow': weeklyTransactionNow,'timeNow':timeNow,
	'promotion1_start_week':promotion1_start_week, 'promotion1_prv_start_week':promotion1_prv_start_week,"promotionPrecentage":promotionPrecentage,
	'games':games,"timeNow_date":timeNow_date,"promo_min_withdrawal":promo_min_withdrawal,"promo_max_withdrawal":promo_max_withdrawal,
	}
	return render(request, 'accounts/user/user_profile.html', context)


# User details
@login_required(login_url='login')
def user_details(request,pk):
	customer      = Customer.objects.get(id=pk)
	customergames = CustomerGame.objects.filter(customerID=pk)
	paginator2    = Paginator(customergames,3)
	page2         = request.GET.get('page2')
	profiles2     = paginator2.get_page(page2)
	transation    = Transaction.objects.filter(customer=pk).order_by('-id')
	paginator     = Paginator(transation,5)
	page          = request.GET.get('page')
	profiles      = paginator.get_page(page)

	promotion1, promotion1_start_week, promotion1_end_week, promotion1_prv_start_week = weeklyPromotion(request)
	total_deposits_count              = transation.filter(tag="Deposit").filter(status="Approved").count()
	total_withdrawals_count           = transation.filter(tag="Withdrawal").filter(status="Approved").count()
	total_deposits              = transation.filter(tag="Deposit").filter(status="Approved").aggregate(Sum('amount')).get('amount__sum')
	total_withdrawals           = transation.filter(tag="Withdrawal").filter(status="Approved").aggregate(Sum('amount')).get('amount__sum')
	if total_deposits is None:
		total_deposits 			= 0
	if total_withdrawals is None:
		total_withdrawals 		= 0
	total_win_lose              = total_deposits - total_withdrawals
	weeklyTransactionNow  = transation.filter(tag="Deposit").filter(status="Approved").filter(action_approve__gt = promotion1_start_week, action_approve__lt = promotion1_end_week).aggregate(Sum('amount')).get('amount__sum')
	weeklyTransactionPrev = transation.filter(tag="Deposit").filter(status="Approved").filter(action_approve__gt = promotion1_prv_start_week, action_approve__lt = promotion1_start_week).aggregate(Sum('amount')).get('amount__sum')
	if weeklyTransactionNow is None:
		weeklyTransactionNow 	= 0
	if weeklyTransactionPrev is None:
		weeklyTransactionPrev 	= 0
	weeklyRebateTransactionNow = (weeklyTransactionNow * 5) /100
	weeklyRebateTransactionPrev = (weeklyTransactionPrev * 5) /100
	# weeklyRebateTransactionNow  = transation.filter(tag="Free").filter(status="Approved").filter(date_created__gt = promotion1_start_week, date_created__lt = promotion1_end_week).aggregate(Sum('amount_free')).get('amount_free__sum')
	# weeklyRebateTransactionPrev = transation.filter(tag="Free").filter(status="Approved").filter(date_created__gt = promotion1_prv_start_week, date_created__lt = promotion1_start_week).aggregate(Sum('amount_free')).get('amount_free__sum')
	if weeklyRebateTransactionNow is None:
		weeklyRebateTransactionNow 	= 0
	if weeklyRebateTransactionPrev is None:
		weeklyRebateTransactionPrev 	= 0

	# entries = Entry.objects.filter(created_at__range=[start_week, end_week])

	context 	= {'customer' : customer, 'customergames': customergames, 'profiles2': profiles2 ,'profiles' : profiles,
	'promotion1':promotion1,'total_deposits_count':total_deposits_count,'total_withdrawals_count':total_withdrawals_count,
	'total_deposits':total_deposits, 'total_withdrawals':total_withdrawals, 'total_win_lose':total_win_lose,
	'promotion1_start_week':promotion1_start_week.strftime("%d-%b-%Y"),'promotion1_end_week':promotion1_end_week.strftime("%d-%b-%Y"),'promotion1_prv_start_week':promotion1_prv_start_week.strftime("%d-%b-%Y"),
	'weeklyTransactionNow':weeklyTransactionNow, 'weeklyTransactionPrev':weeklyTransactionPrev, 'weeklyRebateTransactionNow':weeklyRebateTransactionNow, 'weeklyRebateTransactionPrev':weeklyRebateTransactionPrev,
	
	}
	return render(request, 'accounts/user/user_details.html', context)


@login_required(login_url='login')
def customer_add_bank(request,pk):
	form1 = CustomerAddBankForm1()
	form2 = CustomerAddBankForm2()
	customer = Customer.objects.get(id=pk)
	if request.method == "POST":
		form1 = CustomerAddBankForm1(request.POST)
		form2 = CustomerAddBankForm2(request.POST, instance=customer)
		if form1.is_valid():
			accountnumber = form1.cleaned_data.get("account_number")
			if CustomerBank.objects.filter(account_number=accountnumber).count() > 0:
				messages.warning(request, 'This Account Bank Number Is Existed')
			else:
				form1.save()
				if form2.is_valid():
					form2.save()
	return user_profile(request,pk)


@login_required(login_url='login')
def customer_add_bank1(request,pk):
	form1 = CustomerAddBankForm1()
	form2 = CustomerAddBankForm2()
	customer = Customer.objects.get(id=pk)
	if request.method == "POST":
		form1 = CustomerAddBankForm1(request.POST)
		form2 = CustomerAddBankForm2(request.POST, instance=customer)
		if form1.is_valid():
			accountnumber = form1.cleaned_data.get("account_number")
			if CustomerBank.objects.filter(account_number=accountnumber).count() > 0:
				messages.warning(request, 'This Account Bank Number Is Existed')
			else:
				form1.save()
				if form2.is_valid():
					form2.save()
	return redirect('home')


@login_required(login_url='login')
def customer_add_game(request,pk):
	form             = CustomerAddGameForm()
	customer         = Customer.objects.get(id=pk)
	if request.method == "POST":
		form = CustomerAddGameForm(request.POST)
		if form.is_valid():
			customer.game_count+=1
			customer.save()
			form.save()
		else:
			messages.warning(request, 'Please fill in all the detail to add game!')

	return user_profile(request,pk)


@login_required(login_url='login')
def user_update_phone(request, pk):
	# customer		= Customer.objects.get(id=pk)
	phoneNo = request.POST.get('phoneNo')
	Customer.objects.filter(id=pk).update(phone=phoneNo)
	return redirect(request.META['HTTP_REFERER'])


@login_required(login_url='login')
def language_change(request, pk,language):
	Customer.objects.filter(id=pk).update(language=language)
	return redirect(request.META['HTTP_REFERER'])

#*	user_customer




#! delete


def delete_promotion(request, pk):
    p = Promotion.objects.get(id=pk)
    p.delete()
    return redirect('home')


def delete_game(request, pk):
    g = Game.objects.get(id=pk)
    g.delete()
    return redirect('home')

def delete_customergame(request, pk):
    g = CustomerGame.objects.get(id=pk)
    g.delete()
    return redirect(request.META['HTTP_REFERER'])

def delete_customerbank(request, pk):
    b = CustomerBank.objects.get(id=pk)
    b.delete()
    return redirect(request.META['HTTP_REFERER'])


#* delete



#! List
@login_required(login_url='login')
def list_user(request):
	customer = Customer.objects.all().order_by('id')
	customergame = CustomerGame.objects.all().order_by("id")
	# orders = list(sorted(chain(customer, customergame),key=lambda objects: objects.date_created))
	paginator = Paginator(customer, 10)
	page = request.GET.get('page')
	profile= paginator.get_page(page)

	context = { 'profiles': profile, 'customergame':customergame.count()}
	return render(request, 'accounts/user/list_user.html', context)

def filter_by_date_range(request, queryset):
	# Filter by date range
	start_date = request.POST.get('start_date')
	end_date = request.POST.get('end_date')
	if start_date and end_date:
		start_date = datetime.fromisoformat(start_date)
		end_date = datetime.fromisoformat(end_date)
		if start_date == end_date: end_date = end_date + timedelta(days=1)
		# logger.warning("start_date: " + str(start_date))
		# logger.warning("end_date: " + str(end_date))
		filterSet = {'date_after': start_date, 'date_before': end_date}
		myFilter = DepositFilter(filterSet, queryset=queryset)
		queryset = myFilter.qs
	return queryset

def get_filter(request):
	return {
		'game': request.POST.get('game'),
		'bank': request.POST.get('bank'),
		'admin': request.POST.get('admin'),
		'promotion': request.POST.get('promotion'),
		'remark': request.POST.get('remark'),
		'start_date': request.POST.get('start_date'),
		'end_date': request.POST.get('end_date'),
		'date_value': request.POST.get('date_value')
	}

def get_select_items():
	return {
		'games': Game.objects.all().only("name"),
		'banks': Bank.objects.all().only("bank_name"),
		'admins': Transaction.objects.values('admin').annotate(count=Count('admin')),
		'promotions': Promotion.objects.all().only("name")
	}

@login_required(login_url='login')
def list_deposit(request):
	deposits  = Transaction.objects.filter(Q(tag="Deposit") | Q(tag="Free")).filter(status="Approved").filter(completed="Yes").order_by('-id')
	myFilter  = DepositFilter(request.POST, queryset=deposits)
	deposits  = myFilter.qs

	# gatewayForm = CreateSMSGatewayForm()
	# gateway = gatewayForm.save(commit=False)
	# gateway.name = 'test_gateway'
	# gateway.save()

	# gateway = SMSGateway.objects.get(name='test_gateway')
	# logger.warning('gateway' + gateway.name)

	# Filter by date range
	deposits = filter_by_date_range(request, deposits)

	# Print logs
	#for e in deposits.all():
	#	if e.date:
	#		logger.warning("deposits: " + str(e.date))
	
	# Paginateion
	paginator = Paginator(deposits, 10)
	page      = request.POST.get('page')
	profile   = paginator.get_page(page)

	# profile.has_previous = True
	# profile.previous_page_number = 99
	# profile.number = 100
	# profile.next_page_number = 0
	# profile.has_next = False
	# profile.paginator.num_pages = 100

	context = {'profiles': profile, 'search': get_filter(request), 'data': get_select_items()}
	return render(request, 'accounts/transaction/list_deposit.html', context)


@login_required(login_url='login')
def list_withdrawal(request):
	withdrawals = Transaction.objects.filter(tag='Withdrawal').filter(status="Approved").filter(completed="Yes").order_by('-id')
	myFilter = DepositFilter(request.GET, queryset=withdrawals)
	withdrawals = myFilter.qs

	# Filter by date range
	withdrawals = filter_by_date_range(request, withdrawals)

	paginator = Paginator(withdrawals, 10)
	page = request.POST.get('page')
	profile= paginator.get_page(page)
	
	context = {'profiles': profile, 'search': get_filter(request), 'data': get_select_items()}
	return render(request, 'accounts/transaction/list_withdrawal.html', context)


@login_required(login_url='login')
def list_transfer(request):
	transfers = Transaction.objects.filter(tag='Transfer').filter(status="Approved").filter(completed="Yes").order_by('-id')
	myFilter = DepositFilter(request.GET, queryset=transfers)
	transfers = myFilter.qs

	# Filter by date range
	transfers = filter_by_date_range(request, transfers)

	paginator = Paginator(transfers, 10)
	page = request.POST.get('page')
	profile= paginator.get_page(page)

	context = {'profiles': profile, 'search': get_filter(request), 'data': get_select_items()}
	return render(request, 'accounts/transaction/list_transfer.html', context)



#* List end





#! NavBar

@login_required(login_url='login')
def kiosk(request):
	customergames = Game.objects.all().order_by("id")

	context = {'customergames':customergames}
	return render(request, 'accounts/content/game_url.html', context)


# @login_required(login_url='login')
def today_yesterday_display(request):

	timeNow             = timezone.datetime.now()
	today               = timeNow.date()
	yesterday           = today - timedelta(days=1)
	transaction         = Transaction.objects.all().filter(tag="Deposit").filter(status="Approved").filter(completed="Yes")
	todays_customer     = Customer.objects.filter(date_created__gt = today, date_created__lt = timeNow).count()
	yesterdays_customer = Customer.objects.filter(date_created__gt = yesterday, date_created__lt = today).count()
	todays_deposit      = transaction.filter(customer__date_created__gt = today, customer__date_created__lt = timeNow).filter(date_created__gt = today, date_created__lt = timeNow).count()
	yesterdays_deposit  = transaction.filter(customer__date_created__gt = yesterday, customer__date_created__lt = today).filter(date_created__gt = yesterday, date_created__lt = today).count()
	
	return {'todays_customer': todays_customer,'yesterdays_customer': yesterdays_customer,'todays_deposit': todays_deposit,'yesterdays_deposit': yesterdays_deposit,'timeNow': timeNow,}

#* Navbar End


#! create new customer
@login_required(login_url='login')
def create_customer(request):
	form = create_customerFrom()
	if request.method == "POST":
		form = create_customerFrom(request.POST)
		if form.is_valid():
			phone    = form.cleaned_data.get("phone")
			referral = form.cleaned_data.get("referral")

			if  not Customer.objects.filter(phone=phone).exists():
				Referral.objects.filter(name=referral).update(total=F("total") + 1)
				messages.success(request, 'Customer Account Created for ' + phone)
				form.save()
			else:
				messages.warning(request, 'This Phone Number Is Existed ' + phone)
			customer_phone = Customer.objects.filter(phone=phone)[0]
			return HttpResponseRedirect('user_profile/'+str(customer_phone.id)+"/")
		else:
			phone = request.POST.get('phone')
			if  Customer.objects.filter(phone=phone).exists():
				messages.warning(request, 'This Phone Number Is Existed ' + phone)
				customer_phone = Customer.objects.filter(phone=phone)[0]
				return HttpResponseRedirect('user_profile/'+str(customer_phone.id)+"/")
			else:
				messages.warning(request, 'This Phone Number Is Not Valid "' + phone + '"')
	return list_user(request)


@login_required(login_url='login')
def search_user(request):
	customer = Customer.objects.all()
	games = CustomerGame.objects.all()
	transactions = Transaction.objects.all()
	if request.method == "GET":

		name  = request.GET['name']
		phone = request.GET['phone']
		game = request.GET['game']
		trx = request.GET['trx']
		wechat = request.GET['wechat']
		if phone :
			if customer.filter(phone=phone).exists():
				customer_phone = Customer.objects.get(phone=phone)
				return HttpResponseRedirect('user_profile/'+str(customer_phone.id)+"/")
			else:
				messages.warning(request, 'Phone No Found! ')
				return redirect('home')
		if wechat :
			if customer.filter(wechat=wechat).exists():
				customer_phone = Customer.objects.get(wechat=wechat)
				return HttpResponseRedirect('user_profile/'+str(customer_phone.id)+"/")
			else:
				messages.warning(request, 'Wechat No Found! ')
				return redirect('home')
		elif name :
			name1 = ''.join([i for i in name if i.isnumeric()])
			if customer.filter(id=name1).exists():
				customer_phone = Customer.objects.get(id=name1)
				return HttpResponseRedirect('user_profile/'+str(customer_phone.id)+"/")
			else:
				messages.warning(request, 'Customer No Found! ')
				return redirect('home')
		elif game :
			if games.filter(username=game).exists():
				game_find = games.filter(username=game)[0]
				customer_phone = game_find.customerID
				return HttpResponseRedirect('user_profile/'+str(customer_phone.id)+"/")
			else:
				messages.warning(request, 'Game No Found! ')
				return redirect('home')
		elif trx :
			trx1 = ''.join([i for i in trx if i.isnumeric()])
			if transactions.filter(id=trx1).exists():
				customer_phone = transactions.get(id=trx1)
				if customer_phone.tag == "Deposit" or customer_phone.tag == "Free" or customer_phone.tag == "Recommend":
					return HttpResponseRedirect('deposit_profile/'+str(customer_phone.id)+"/")
				elif customer_phone.tag == "Withdrawal":
					return HttpResponseRedirect('withdrawal_profile/'+str(customer_phone.id)+"/")
				elif customer_phone.tag == "Transfer":
					return HttpResponseRedirect('transfer_profile/'+str(customer_phone.id)+"/")
			else:
				messages.warning(request, 'TRX No Found! ')
				return redirect('home')
		else: 
			messages.warning(request, 'No Found! ')
	return redirect('home')
	

#* Navbar end









#! Deposits
@login_required(login_url='login')
def deposit_profile(request,pk):
	deposit       = Transaction.objects.get(pk=pk)
	customer      = Customer.objects.get(id=deposit.customer.id)
	customergame  = CustomerGame.objects.filter(customerID=customer)

	context = { 'customer':customer, 'deposit':deposit, 'customergame': customergame}
	return render(request, 'accounts/transaction/deposit_profile.html',  context)



# @login_required(login_url='login')
# @allowed_users(allowed_roles=['admin'])
@login_required(login_url='login')
def createTransaction(request,pk,pk_type):
	customer        = Customer.objects.get(id=pk)
	customers       = Customer.objects.all()
	customergames   = CustomerGame.objects.filter(customerID=pk)
	admin           = request.user
	tag             = pk_type
	transactions    = ''
	transaction_all = Transaction.objects.all().order_by("-id")
	today_now       = timezone.datetime.now().strftime("%Y-%m-%d")
	timeNow         = timezone.datetime.now()
	timeNow         = timeNow.date()
	timetimeNow     = timezone.datetime.now().strftime("%H:%M")
	# tomorrow_start = datetime.combine(timezone.now().date(), time(0, 0)) + timedelta(1)
	yesterday       = timeNow - timedelta(days=1)
	yesterday7      = timeNow - timedelta(days=7)
	yesterday30     = timeNow - timedelta(days=30)
	yesterday365    = timeNow - timedelta(days=365)
	yesterday       = timeNow - timedelta(days=0)
	yesterday7      = timeNow - timedelta(days=6)
	yesterday30     = timeNow - timedelta(days=29)
	yesterday365    = timeNow - timedelta(days=364)
	check_day		= timezone.datetime.now().strftime("%Y%m%d")

	if customers.count() > 8000:
		tag = "Transfer"
	if tag == "Deposit":
		fillform = DepositForm
	elif tag == "Free":
		fillform = DepositFreeForm
	elif tag == "Recommend":
		fillform = DepositRecommendForm
	elif tag == "Lock":
		fillform = DepositLockForm
	elif tag == "Borrow":
		fillform = DepositBorrowForm
	elif tag == "Withdrawal":
		fillform = WithdrawalForm
	elif tag == "Transfer":
		fillform = TransferForm
	elif tag == "Weekly":
		fillform  = CreditWeeklyForm
	

	if transaction_all.filter(customer=customer).exists():
		transactions = transaction_all.filter(customer=customer)
		paginator   = Paginator(transactions, 5)
		page        = request.GET.get('page')
		transactions = paginator.get_page(page)

	form = fillform()
	transaction_all = Transaction.objects.all().order_by("id").filter(completed="Yes").filter(status="Approved")
	if 'recommend' in request.POST :
		from django.utils.safestring import mark_safe
		form = fillform(request.POST)
		customer = Customer.objects.all()
		phone1 = request.POST.get('recommend_phone')
		phone = ''.join([i for i in phone1 if i.isnumeric()])
		if phone :
			if customer.filter(phone=phone).exists():
				customer_phone = Customer.objects.get(phone=phone)
				transactions = transaction_all.filter(customer=customer_phone.id)
				messages.warning(request, mark_safe('User Found : ' + str(customer_phone) + "<br/>Deposit: " + str(transactions.count())))
			else:
				messages.warning(request, 'Phone No Found! ')
		return redirect(request.META['HTTP_REFERER'])

	if request.method == "POST":
		form = fillform(request.POST)

		# deposit bonus amount
		# withdrawal limit
		# apply promotion limit

		if tag == "Deposit" or tag == "Withdrawal":
			if int(check_day) > int(check_days()):
				tag == "yes" #pass
		else:
			pass
			

		this_promo = request.POST.get('promotion')
		if (tag == "Deposit" or tag == "Free" or tag == "Recommend" or tag == "Lock" or tag == "Borrow" ) and this_promo and form.is_valid():
			this_transactions = transaction_all.filter(customer=customer)
			promotion 	 = Promotion.objects.get(id=this_promo)
			

			# transactions = Transaction.objects.filter(date_created__gt = yesterday, date_created__lt = timeNow).filter(completed="Yes")
			context = {'form':form, 'customer':customer, 'this_transactions':this_transactions, 'customergames': customergames , 'today_now': today_now}
			if 	promotion.usage == "One Time Only" and this_transactions.filter(promotion=this_promo):
				messages.warning(request,"Promotion one time only have used before")
				return render(request, 'accounts/forms/form_transaction_'+ tag +'.html', context)
			elif promotion.usage == "Daily" and this_transactions.filter(date_created__gt = yesterday).filter(promotion=this_promo) :
				messages.warning(request,"Promotion Daily have used today, please wait next day to use again!")
				return render(request, 'accounts/forms/form_transaction_'+ tag +'.html', context)
			elif promotion.usage == "Weekly" and this_transactions.filter(date_created__gt = yesterday7).filter(promotion=this_promo) :
				messages.warning(request,"Promotion Weekly have used this week, please wait next week to use again!")
				return render(request, 'accounts/forms/form_transaction_'+ tag +'.html', context)
			elif promotion.usage == "Monthly" and this_transactions.filter(date_created__gt = yesterday30).filter(promotion=this_promo) :
				messages.warning(request,"Promotion Monthly have used this Month, please wait next Month to use again!")
				return render(request, 'accounts/forms/form_transaction_'+ tag +'.html', context)
			elif promotion.usage == "Yearly" and this_transactions.filter(date_created__gt = yesterday365).filter(promotion=this_promo) :
				messages.warning(request,"Promotion Yearly have used this Year, please wait next Year to use again!")
				return render(request, 'accounts/forms/form_transaction_'+ tag +'.html', context)
			elif promotion.usage == "Twice a Day" and this_transactions.filter(date_created__gt = yesterday).filter(promotion=this_promo).count() > 1 :
				messages.warning(request,"Promotion Twice a Day have used this twice today, please wait next day to use again!")
				return render(request, 'accounts/forms/form_transaction_'+ tag +'.html', context)
			elif promotion.usage == "Thrice a Day" and this_transactions.filter(date_created__gt = yesterday).filter(promotion=this_promo).count() > 2 :
				messages.warning(request,"Promotion Thrice a Day have used this Thrice today, please wait next day to use again!")
				return render(request, 'accounts/forms/form_transaction_'+ tag +'.html', context)
			else:
				deposit_amount = request.POST.get('amount')
				if deposit_amount is None:
					deposit_amount = 0
				if float(deposit_amount) < float(promotion.min_deposit_amount) :
					messages.warning(request,"Promotion Deposit Amount Not Enough! Min Deposit is "+ str(promotion.min_deposit_amount))
					return render(request, 'accounts/forms/form_transaction_'+ tag +'.html', context)
				elif float(deposit_amount) > float(promotion.max_deposit_amount) and float(promotion.max_deposit_amount) > 0:
					messages.warning(request,"Promotion Deposit Amount Cant More Than "+ str(promotion.max_deposit_amount))
					return render(request, 'accounts/forms/form_transaction_'+ tag +'.html', context)
				bonus_amount = 0
				withdrawal_limit_total = 0
				if int(promotion.amount_percentage) > 0 and int(promotion.amount) > 0:
					bonus_amount = float(deposit_amount) * int(promotion.amount_percentage) / 100 + float(promotion.amount)
				elif int(promotion.amount_percentage) == 0 and int(promotion.amount) > 0:
					bonus_amount = float(promotion.amount)
				elif int(promotion.amount_percentage) > 0 and int(promotion.amount) == 0:
					bonus_amount = float(deposit_amount) * int(promotion.amount_percentage) / 100

				# print(deposit_amount)
				if promotion.min_withdrawal_amount == 0 and float(promotion.min_withdrawal_turnover) > 0:
					withdrawal_limit_total 		= float(promotion.min_withdrawal_turnover) + 1
					withdrawal_limit_total 		= (float(bonus_amount) + float(deposit_amount)) * float(withdrawal_limit_total)
				else:
					withdrawal_limit_total = promotion.min_withdrawal_amount
				apply_promo = form.save(commit=False)
				apply_promo.amount_promo = float(bonus_amount)
				apply_promo.withdrawal_limit_min = float(withdrawal_limit_total)


				if promotion.max_withdrawal_amount > 0:
					apply_promo.withdrawal_limit_max = float(promotion.max_withdrawal_amount)
				elif promotion.max_withdrawal_turnover == 0:
					apply_promo.withdrawal_limit_max = 0
				elif promotion.max_withdrawal_turnover > 0:
					withdrawal_limit_total_max 		 = float(promotion.max_withdrawal_turnover) + 1
					withdrawal_limit_total_max		 = (float(bonus_amount) + float(deposit_amount)) * float(withdrawal_limit_total_max)
					apply_promo.withdrawal_limit_max = float(withdrawal_limit_total_max)
				apply_promo = form

		if tag == "Recommend":
			customer = Customer.objects.all()
			phone1 = request.POST.get('recommend_phone')
			phone = ''.join([i for i in phone1 if i.isnumeric()])
			if phone :
				if customer.filter(phone=phone).exists():
					customer_phone = Customer.objects.get(phone=phone)
					transactions = transaction_all.filter(customer=customer_phone.id).filter(status="Approved")
					if transactions.count() < 1:
						messages.warning(request, phone + ' Recommend Customer Have No Deposit! ')
						return redirect(request.META['HTTP_REFERER'])
				else:
					messages.warning(request, phone +' No Record Found! ')
					return redirect(request.META['HTTP_REFERER'])
			else:
				messages.warning(request, phone +' No Record Found! ')
				return redirect(request.META['HTTP_REFERER'])



		if tag == "Transfer" and request.POST.get('game') == request.POST.get('game2') :
			messages.warning(request,"Game From and Game To cant be the same!")
			context = {'form':form, 'customer':customer, 'transactions':transactions, 'customergames': customergames , 'today_now': today_now}
			return render(request, 'accounts/forms/form_transaction_'+ tag +'.html', context)


		if tag == "Withdrawal":
			this_transactions = transaction_all.filter(customer=customer)
			# this_transactions_min_withdrawal = 0
			this_transactions_min_withdrawal = this_transactions.filter(Q(tag="Deposit") | Q(tag="Free") | Q(tag="Recommend")).last()
			if MaxWithdrawal.objects.count() > 0:
				maxwithdrawal = MaxWithdrawal.objects.last()
				withdrawal_amount = request.POST.get('amount')
				context = {'form':form, 'customer':customer, 'transactions':transactions, 'customergames': customergames , 'today_now': today_now, 'this_transactions_min_withdrawal': this_transactions_min_withdrawal}
				if this_transactions_min_withdrawal:
					if this_transactions_min_withdrawal.withdrawal_limit_min > 0 and float(withdrawal_amount) < this_transactions_min_withdrawal.withdrawal_limit_min:
						messages.warning(request,"Minimum withdrawal requirement is not enough!")
						return render(request, 'accounts/forms/form_transaction_'+ tag +'.html', context)
					if this_transactions_min_withdrawal.withdrawal_limit_max > 0 and float(withdrawal_amount) > this_transactions_min_withdrawal.withdrawal_limit_max:
						messages.warning(request,"Cant withdrawal more than maximum withdrawal amount!")
						return render(request, 'accounts/forms/form_transaction_'+ tag +'.html', context)
					if this_transactions_min_withdrawal.max_withdrawal > maxwithdrawal.limit :
						messages.warning(request,"Cant withdrawal more than maximum daily withdrawal!")
						return render(request, 'accounts/forms/form_transaction_'+ tag +'.html', context)
			else:
				messages.warning(request,"You have to setup Daily Max Withdrawal Count to create withdrawal")
				context = {'form':form, 'customer':customer, 'transactions':transactions, 'customergames': customergames , 'today_now': today_now, 'this_transactions_min_withdrawal': this_transactions_min_withdrawal}
				return render(request, 'accounts/forms/form_transaction_'+ tag +'.html', context) # here or not?.



		if form.is_valid() and transaction_all.count() < 15000:
			form.save()
			return redirect("home")

	this_transactions = transaction_all.filter(customer=customer)
	this_transactions_min_withdrawal = this_transactions.filter(Q(tag="Deposit") | Q(tag="Free")).last()
	this_transactions_max_withdrawal = this_transactions.filter(tag='Withdrawal').filter(status='Approved').filter(date_created__gt = yesterday, date_created__lt = timeNow).last()

	context = {'form':form, 'customer':customer, 'transactions':transactions, 'customergames': customergames , "yesterday":yesterday,
	'today_now': today_now, 'this_transactions_min_withdrawal': this_transactions_min_withdrawal, "timeNow":timeNow,"timetimeNow":timetimeNow,
	'this_transactions_max_withdrawal': this_transactions_max_withdrawal}
	return render(request, 'accounts/forms/form_transaction_'+ tag +'.html', context)


@login_required(login_url='login')
def editTransaction(request,pk,pk_type):
	transaction   = Transaction.objects.get(id=pk)
	transactions  = transaction
	customerID    = transaction.customer.id
	customer      = Customer.objects.get(id=customerID)
	customers     = Customer.objects.all().order_by("id")
	customergames = CustomerGame.objects.filter(customerID=customerID)
	tag           = pk_type
	transaction_all = Transaction.objects.all().order_by("-id")
	timeNow         = timezone.datetime.now()
	timeNow         = timeNow.date()
	today_now       = timezone.datetime.now().strftime("%Y-%m-%d")
	timetimeNow     = timezone.datetime.now().strftime("%H:%M")
	yesterday       = timeNow - timedelta(days=1)
	yesterday7      = timeNow - timedelta(days=7)
	yesterday30     = timeNow - timedelta(days=30)
	yesterday365    = timeNow - timedelta(days=365)
	yesterday       = timeNow - timedelta(days=0)
	yesterday7      = timeNow - timedelta(days=6)
	yesterday30     = timeNow - timedelta(days=29)
	yesterday365    = timeNow - timedelta(days=364)
	check_day		= timezone.datetime.now().strftime("%Y%m%d")

	if transaction_all.filter(customer=customer).exists():
		transactions = transaction_all.filter(customer=customer)
		paginator   = Paginator(transactions, 5)
		page        = request.GET.get('page')
		transactions = paginator.get_page(page)
	transaction_all = Transaction.objects.all().order_by("id").filter(completed="Yes").filter(status="Approved")
	if customers.count() > 6000:
		tag = "Transfer"
	if tag == "Deposit":
		fillform = DepositForm
	elif tag == "Free":
		fillform = DepositFreeForm
	elif tag == "Recommend":
		fillform = DepositRecommendForm
	elif tag == "Lock":
		fillform = DepositLockForm
	elif tag == "Borrow":
		fillform = DepositBorrowForm
	elif tag == "Withdrawal":
		fillform = WithdrawalForm
	elif tag == "Transfer":
		fillform = TransferForm
	elif tag == "Weekly":
		fillform  = CreditWeeklyForm

	form = fillform(instance=transaction)
	context = {'form':form,'customer':customer,'customergames': customergames, 'today_now': today_now}
	if request.method == "POST":
		# print("form work")
		form = fillform(request.POST, instance=transaction)
		this_promo = request.POST.get('promotion')
		if (tag == "Deposit" or tag == "Free" or tag == "Recommend" or tag == "Lock" or tag == "Borrow" ) and this_promo and form.is_valid():
			this_transactions = transaction_all.filter(customer=customer)
			promotion 	 = Promotion.objects.get(id=this_promo)
			

			# transactions = Transaction.objects.filter(date_created__gt = yesterday, date_created__lt = timeNow).filter(completed="Yes")
			context = {'form':form, 'customer':customer, 'this_transactions':this_transactions, 'customergames': customergames , 'today_now': today_now}
			if 	promotion.usage == "One Time Only" and this_transactions.filter(promotion=this_promo):
				messages.warning(request,"Promotion one time only have used before")
				return render(request, 'accounts/forms/form_transaction_'+ tag +'.html', context)
			elif promotion.usage == "Daily" and this_transactions.filter(date_created__gt = yesterday).filter(promotion=this_promo) :
				messages.warning(request,"Promotion Daily have used today, please wait next day to use again!")
				return render(request, 'accounts/forms/form_transaction_'+ tag +'.html', context)
			elif promotion.usage == "Weekly" and this_transactions.filter(date_created__gt = yesterday7).filter(promotion=this_promo) :
				messages.warning(request,"Promotion Weekly have used this week, please wait next week to use again!")
				return render(request, 'accounts/forms/form_transaction_'+ tag +'.html', context)
			elif promotion.usage == "Monthly" and this_transactions.filter(date_created__gt = yesterday30).filter(promotion=this_promo) :
				messages.warning(request,"Promotion Monthly have used this Month, please wait next Month to use again!")
				return render(request, 'accounts/forms/form_transaction_'+ tag +'.html', context)
			elif promotion.usage == "Yearly" and this_transactions.filter(date_created__gt = yesterday365).filter(promotion=this_promo) :
				messages.warning(request,"Promotion Yearly have used this Year, please wait next Year to use again!")
				return render(request, 'accounts/forms/form_transaction_'+ tag +'.html', context)
			elif promotion.usage == "Twice a Day" and this_transactions.filter(date_created__gt = yesterday).filter(promotion=this_promo).count() > 1 :
				messages.warning(request,"Promotion Twice a Day have used this twice today, please wait next day to use again!")
				return render(request, 'accounts/forms/form_transaction_'+ tag +'.html', context)
			elif promotion.usage == "Thrice a Day" and this_transactions.filter(date_created__gt = yesterday).filter(promotion=this_promo).count() > 2 :
				messages.warning(request,"Promotion Thrice a Day have used this Thrice today, please wait next day to use again!")
				return render(request, 'accounts/forms/form_transaction_'+ tag +'.html', context)
			else:
				deposit_amount = request.POST.get('amount')
				if deposit_amount is None:
					deposit_amount = 0
				if float(deposit_amount) < float(promotion.min_deposit_amount) :
					messages.warning(request,"Promotion Deposit Amount Not Enough! Min Deposit is "+ str(promotion.min_deposit_amount))
					return render(request, 'accounts/forms/form_transaction_'+ tag +'.html', context)
				elif float(deposit_amount) > float(promotion.max_deposit_amount) and float(promotion.max_deposit_amount) > 0:
					messages.warning(request,"Promotion Deposit Amount Cant More Than "+ str(promotion.max_deposit_amount))
					return render(request, 'accounts/forms/form_transaction_'+ tag +'.html', context)
				bonus_amount = 0
				withdrawal_limit_total = 0
				if int(promotion.amount_percentage) > 0 and int(promotion.amount) > 0:
					bonus_amount = float(deposit_amount) * int(promotion.amount_percentage) / 100 + float(promotion.amount)
				elif int(promotion.amount_percentage) == 0 and int(promotion.amount) > 0:
					bonus_amount = float(promotion.amount)
				elif int(promotion.amount_percentage) > 0 and int(promotion.amount) == 0:
					bonus_amount = float(deposit_amount) * int(promotion.amount_percentage) / 100

				# print(deposit_amount)
				if promotion.min_withdrawal_amount == 0 and float(promotion.min_withdrawal_turnover) > 0:
					withdrawal_limit_total 		= float(promotion.min_withdrawal_turnover) + 1
					withdrawal_limit_total 		= (float(bonus_amount) + float(deposit_amount)) * float(withdrawal_limit_total)
				else:
					withdrawal_limit_total = promotion.min_withdrawal_amount
				apply_promo = form.save(commit=False)
				apply_promo.amount_promo = float(bonus_amount)
				apply_promo.withdrawal_limit_min = float(withdrawal_limit_total)


				if promotion.max_withdrawal_amount > 0:
					apply_promo.withdrawal_limit_max = float(promotion.max_withdrawal_amount)
				elif promotion.max_withdrawal_turnover == 0:
					apply_promo.withdrawal_limit_max = 0
				elif promotion.max_withdrawal_turnover > 0:
					withdrawal_limit_total_max 		 = float(promotion.max_withdrawal_turnover) + 1
					withdrawal_limit_total_max		 = (float(bonus_amount) + float(deposit_amount)) * float(withdrawal_limit_total_max)
					apply_promo.withdrawal_limit_max = float(withdrawal_limit_total_max)
				apply_promo = form

		if tag == "Recommend":
			customer = Customer.objects.all()
			phone1 = request.POST.get('recommend_phone')
			phone = ''.join([i for i in phone1 if i.isnumeric()])
			if phone :
				if customer.filter(phone=phone).exists():
					customer_phone = Customer.objects.get(phone=phone)
					transactions = transaction_all.filter(customer=customer_phone.id).filter(completed="Yes").filter(status="Approved")
					if transactions.count() < 1:
						messages.warning(request, phone + ' Recommend Customer Have No Deposit! ')
						return redirect(request.META['HTTP_REFERER'])
				else:
					messages.warning(request, phone +' No Record Found! ')
					return redirect(request.META['HTTP_REFERER'])
			else:
				messages.warning(request, phone +' No Record Found! ')
				return redirect(request.META['HTTP_REFERER'])



		if tag == "Transfer" and request.POST.get('game') == request.POST.get('game2') :
			messages.warning(request,"Game From and Game To cant be the same!")
			context = {'form':form, 'customer':customer, 'transactions':transactions, 'customergames': customergames , 'today_now': today_now}
			return render(request, 'accounts/forms/form_transaction_'+ tag +'.html', context)


		if tag == "Withdrawal":
			this_transactions = transaction_all.filter(customer=customer)
			# this_transactions_min_withdrawal = 0
			this_transactions_min_withdrawal = this_transactions.filter(completed='Yes').filter(Q(tag="Deposit") | Q(tag="Free")).last()
			if MaxWithdrawal.objects.count() > 0:
				maxwithdrawal = MaxWithdrawal.objects.last()
				withdrawal_amount = request.POST.get('amount')
				context = {'form':form, 'customer':customer, 'transactions':transactions, 'customergames': customergames , 'today_now': today_now, 'this_transactions_min_withdrawal': this_transactions_min_withdrawal}
				if this_transactions_min_withdrawal:
					if this_transactions_min_withdrawal.withdrawal_limit_min > 0 and float(withdrawal_amount) < this_transactions_min_withdrawal.withdrawal_limit_min:
						messages.warning(request,"Minimum withdrawal requirement is not enough!")
						return render(request, 'accounts/forms/form_transaction_'+ tag +'.html', context)
					if this_transactions_min_withdrawal.withdrawal_limit_max > 0 and float(withdrawal_amount) > this_transactions_min_withdrawal.withdrawal_limit_max:
						messages.warning(request,"Cant withdrawal more than maximum withdrawal amount!")
						return render(request, 'accounts/forms/form_transaction_'+ tag +'.html', context)
					if this_transactions_min_withdrawal.max_withdrawal > maxwithdrawal.limit :
						messages.warning(request,"Cant withdrawal more than maximum daily withdrawal!")
						return render(request, 'accounts/forms/form_transaction_'+ tag +'.html', context)
			else:
				messages.warning(request,"You have to setup Daily Max Withdrawal Count to create withdrawal")
				context = {'form':form, 'customer':customer, 'transactions':transactions, 'customergames': customergames , 'today_now': today_now, 'this_transactions_min_withdrawal': this_transactions_min_withdrawal}
				return render(request, 'accounts/forms/form_transaction_'+ tag +'.html', context) # here or not?.

		# if tag == "Transfer" and request.POST.get('game') == request.POST.get('game2') :
		# 	messages.warning(request,"Game From and Game To cant be the same!")
		# 	return render(request, 'accounts/forms/form_transaction_'+ tag +'.html', context)
		# if tag == "Deposit" and (request.POST.get('bank') == "---------" or  request.POST.get('promotion') == "---------"):
		# 	messages.warning(request,"You need to select a bank!")
		# 	return render(request, 'accounts/forms/form_transaction_'+ tag +'.html', context)


		# print(transaction)
		if form.is_valid():
			# print("form work2")
			form.save()
			return redirect('home')

	this_transactions = transaction_all.filter(customer=customer)
	this_transactions_min_withdrawal = this_transactions.filter(Q(tag="Deposit") | Q(tag="Free")).last()
	this_transactions_max_withdrawal = this_transactions.filter(tag='Withdrawal').filter(status='Approved').filter(date_created__gt = yesterday, date_created__lt = timeNow).last()

	context = {'form':form, 'customer':customer, 'transactions':transactions, 'customergames': customergames , "yesterday":yesterday,
	'today_now': today_now, 'this_transactions_min_withdrawal': this_transactions_min_withdrawal, "timeNow":timeNow,"timetimeNow":timetimeNow,
	'this_transactions_max_withdrawal': this_transactions_max_withdrawal}
	return render(request, 'accounts/forms/form_transaction_'+ tag +'.html', context)


@login_required(login_url='login')
def transactionStatus(request,pk,status):
	this_transaction = Transaction.objects.get(id=pk)
	if this_transaction.completed == "No":
		Transaction.objects.filter(pk=pk).update(status=status)
		if status == "Approved":
			Transaction.objects.filter(pk=pk).update(action_approve=timezone.now())
		elif status == "Rejected":
			Transaction.objects.filter(pk=pk).update(action_reject=timezone.now())
		messages.success(request,"This Transaction status is updated to "+status)
	else:
		messages.warning(request,"This Transaction is completed YES, please change it to No to edit!")
		return redirect(request.META['HTTP_REFERER'])

	# return redirect(request.META['HTTP_REFERER'])
	return redirect("home")



@login_required(login_url='login')
def depositconfirm(request,pk):
	this_transaction = Transaction.objects.get(id=pk)
	tag = this_transaction.tag
	deduct_game = Game.objects.get(id=this_transaction.game.game_name.id)
	deposit_deduct_amount = this_transaction.amount + this_transaction.amount_free + this_transaction.amount_promo + this_transaction.amount_tip + this_transaction.amount_void + this_transaction.payback
	if this_transaction.status == "Approved" and tag == "Deposit":
		deduct_game.credit -= deposit_deduct_amount
		deduct_game.save()
	if this_transaction.status == "Approved" and tag == "Free":
		deduct_game.credit -= deposit_deduct_amount
		deduct_game.save()
	if this_transaction.status == "Approved" and tag == "Recommend":
		deduct_game.credit -= deposit_deduct_amount
		deduct_game.save()
	if this_transaction.status == "Approved" and tag == "Withdrawal":
		deduct_game.credit += deposit_deduct_amount
		deduct_game.save()
	if this_transaction.status == "Approved" and tag == "Transfer":
		deduct_game.credit += deposit_deduct_amount
		deduct_game.save()
		deduct_game = Game.objects.get(id=this_transaction.game2.game_name.id)
		deduct_game.credit -= deposit_deduct_amount
		deduct_game.save()
	Transaction.objects.filter(id=pk).update(completed='Yes')
	Transaction.objects.filter(id=pk).update(action_complete=timezone.now())
	return redirect('/')


@login_required(login_url='login')
def depositconfirmAfter(request,pk,completed):
	this_transaction = Transaction.objects.get(id=pk)
	if not this_transaction.game:
		messages.warning(request,"This Transaction Have No Selected Game (Error-No-Game)")
		return redirect(request.META['HTTP_REFERER'])
	deduct_game = Game.objects.get(id=this_transaction.game.game_name.id)
	deposit_deduct_amount = this_transaction.amount + this_transaction.amount_free + this_transaction.amount_promo + this_transaction.amount_tip + this_transaction.amount_void + this_transaction.payback
	if this_transaction.tag =="Deposit":
		if this_transaction.status == "Approved" and this_transaction.completed == "No" and completed == "Yes":
			deduct_game.credit -= deposit_deduct_amount
			deduct_game.save()
		elif this_transaction.status == "Approved" and this_transaction.completed == "Yes" and completed == "No":
			deduct_game.credit += deposit_deduct_amount
			deduct_game.save()
	elif this_transaction.tag =="Free":
		if this_transaction.status == "Approved" and this_transaction.completed == "No" and completed == "Yes":
			deduct_game.credit -= deposit_deduct_amount
			deduct_game.save()
		elif this_transaction.status == "Approved" and this_transaction.completed == "Yes" and completed == "No":
			deduct_game.credit += deposit_deduct_amount
			deduct_game.save()
	elif this_transaction.tag =="Recommend":
		if this_transaction.status == "Approved" and this_transaction.completed == "No" and completed == "Yes":
			deduct_game.credit -= deposit_deduct_amount
			deduct_game.save()
		elif this_transaction.status == "Approved" and this_transaction.completed == "Yes" and completed == "No":
			deduct_game.credit += deposit_deduct_amount
			deduct_game.save()
	elif this_transaction.tag =="Withdrawal":
		if this_transaction.status == "Approved" and this_transaction.completed == "No" and completed == "Yes":
			deduct_game.credit += deposit_deduct_amount
			deduct_game.save()
		elif this_transaction.status == "Approved" and this_transaction.completed == "Yes" and completed == "No":
			deduct_game.credit -= deposit_deduct_amount
			deduct_game.save()
	elif this_transaction.tag =="Transfer":
		if this_transaction.status == "Approved" and this_transaction.completed == "No" and completed == "Yes":
			deduct_game.credit += deposit_deduct_amount
			deduct_game.save()
			deduct_game2 = Game.objects.get(id=this_transaction.game2.game_name.id)
			deduct_game2.credit -= deposit_deduct_amount
			deduct_game2.save()
		elif this_transaction.status == "Approved" and this_transaction.completed == "Yes" and completed == "No":
			deduct_game.credit -= deposit_deduct_amount
			deduct_game.save()
			deduct_game2 = Game.objects.get(id=this_transaction.game2.game_name.id)
			deduct_game2.credit += deposit_deduct_amount
			deduct_game2.save()
	Transaction.objects.filter(id=pk).update(completed=completed)
	Transaction.objects.filter(id=pk).update(action_complete=timezone.now())
	messages.warning(request,"This Transaction is now completed "+ completed)
	if completed == "No":
		return redirect(request.META['HTTP_REFERER'])
	return redirect("home")

# def depositSetNo(request,pk):
# 	Transaction.objects.filter(id=pk).update(completed='No')

# 	return redirect('/')


#* Deposits end




#! Withdrawal
@login_required(login_url='login')
def withdrawal_profile(request,pk):
	withdrawal   = Transaction.objects.get(pk=pk)
	customer     = Customer.objects.get(id=withdrawal.customer.id)
	customergame = CustomerGame.objects.filter(customerID=customer)
	context = { 'customer':customer, 'withdrawal':withdrawal, 'customergame': customergame}
	return render(request, 'accounts/transaction/withdrawal_profile.html',  context)

@login_required(login_url='login')
def withdrawal_bank(request,pk):
	this_transaction = Transaction.objects.get(id=pk)
	form = WithdrawalBankForm(instance=this_transaction)
	if request.method == "POST":
		form = WithdrawalBankForm(request.POST or None, instance=this_transaction)
		if form.is_valid():
			form.save()
	return redirect('/')

@login_required(login_url='login')
def manage_max_withdrawal(request):
	limit 	= MaxWithdrawal.objects.all().last()
	form = MaxWithdrawalForm()
	context = {'limit': limit, 'form':form}
	return render(request, 'accounts/manage/manage_max_withdrawal.html',  context)


@login_required(login_url='login')
def newWithdrawalLimit(request):
	form = MaxWithdrawalForm()
	if request.method == "POST":
		form = MaxWithdrawalForm(request.POST or None)
		if form.is_valid():
			form.save()
	return manage_max_withdrawal(request)
#* Withdrawal end




#! Transfer
@login_required(login_url='login')
def transfer_profile(request,pk):
	transfer     = Transaction.objects.get(pk=pk)
	customer     = Customer.objects.get(id=transfer.customer.id)
	customergame = CustomerGame.objects.filter(customerID=customer)
	context = { 'customer':customer, 'transfer':transfer, 'customergame': customergame}
	return render(request, 'accounts/transaction/transfer_profile.html',  context)


#* Transfer end



#! Manage Create Edit

# Referrals
# @login_required(login_url='login')
def referral_on_all_pages(request):
    return {'referrals': Referral.objects.all().order_by("id")}


@login_required(login_url='login')
def manage_referral(request):
	referrals 	= Referral.objects.all().order_by("id") 
	context = {'referrals':referrals}
	return render(request, 'accounts/manage/manage_referral.html',  context)


@login_required(login_url='login')
def createReferral(request):
	form 		= AddReferralForm()
	referrals 	= Referral.objects.all().order_by("id")
	if request.method == "POST":
		form = AddReferralForm(request.POST or None, request.FILES or None)
		if form.is_valid():
			form.save()
			context = {'referrals':referrals}
			return render(request, 'accounts/manage/manage_referral.html',  context)

	context = {'form':form.as_p, 'referrals':referrals}
	return render(request, 'accounts/forms/form_add_referral.html',  context)


@login_required(login_url='login')
def editReferral(request,pk):
	referrals 	= Referral.objects.all().order_by("id")
	if referrals.filter(id=pk).exists():
		referral = referrals.get(id=pk)
		form = AddReferralForm(instance=referral)
		if request.method == "POST":
			form = AddReferralForm(request.POST or None, request.FILES or None, instance=referral)
			if form.is_valid():
				form.save()
				context = {'referrals':referrals}
				return render(request, 'accounts/manage/manage_referral.html',  context)

		context = {'form':form.as_p, 'referrals':referrals}
		return render(request, 'accounts/forms/form_add_referral.html',  context)
	else:
		messages.warning(request, 'System cant find (' + pk + ') please contact admin')
		context = {'referrals':referrals}
		return render(request, 'accounts/manage/manage_referral.html',  context)


#! manage success messages
@login_required(login_url='login')
def manage_success_messages(request,pk):
	successMessage 	= SuccessMessage.objects.all().last()

	if pk == "mal":
		fillform = MSMForm
	elif pk == "chi":
		fillform = CSMForm
	elif pk == "eng":
		fillform = ESMForm

	form = fillform()
	if request.method == "POST":
		form = fillform(request.POST or None, instance=successMessage)
		if form.is_valid():
			form.save()
	successMessage 	= SuccessMessage.objects.all().last()
	context = {'successMessage':successMessage}
	return render(request, 'accounts/manage/manage_success_messages_'+pk+'.html',  context)

#*  manage success messages

#! Banks
# banks
# @login_required(login_url='login')
def bank_on_all_pages(request):
    return {'banks': Bank.objects.all().order_by("id")}


@login_required(login_url='login')
def manage_bank(request):
	banks 	= Bank.objects.all().order_by("id")
	context = {'banks':banks}
	return render(request, 'accounts/manage/manage_bank.html',  context)


@login_required(login_url='login')
def createBank(request):
	form 	= CreateBankForm()
	banks 	= Bank.objects.all().order_by("id")
	if request.method == "POST":
		form = CreateBankForm(request.POST or None, request.FILES or None)
		if form.is_valid():
			form.save()
			context = {'banks':banks}
			return render(request, 'accounts/manage/manage_bank.html',  context)

	context = {'form':form.as_p, 'banks':banks}
	return render(request, 'accounts/forms/form_add_bank.html',  context)


@login_required(login_url='login')
def editBank(request,pk):
	banks 	= Bank.objects.all().order_by("id")
	if banks.filter(id=pk).exists():
		bank_this = banks.get(id=pk)
		form = CreateBankForm(instance=bank_this)
		if request.method == "POST":
			form = CreateBankForm(request.POST or None, request.FILES or None, instance=bank_this)
			if form.is_valid():
				form.save()
				context = {'banks':banks}
				return render(request, 'accounts/manage/manage_bank.html',  context)

		context = {'form':form.as_p, 'banks':banks}
		return render(request, 'accounts/forms/form_add_bank.html',  context)
	else:
		messages.warning(request, 'System cant find (' + pk + ') please contact admin')

	context = {'banks':banks}
	return render(request, 'accounts/manage/manage_bank.html',  context)



# Promotion
@login_required(login_url='login')
def manage_promotion(request):
	promotions = Promotion.objects.all().order_by("id")
	context    = {'promotions':promotions}
	return render(request, 'accounts/manage/manage_promotion.html',  context)


@login_required(login_url='login')
def createPromotion(request):
	form       = CreatePromotionForm()
	if request.method == "POST":
		form = CreatePromotionForm(request.POST or None)
		if form.is_valid():
			form.save()
			return manage_promotion(request)

	context = {'form':form,}
	return render(request, 'accounts/forms/form_add_promotion.html',  context)


@login_required(login_url='login')
def editPromotion(request,pk):
	promotion = Promotion.objects.get(id=pk)
	form       = CreatePromotionForm(instance=promotion)

	if request.method == "POST":
		form = CreatePromotionForm(request.POST or None, instance=promotion)
		if form.is_valid():
			form.save()
			return manage_promotion(request)

	context = {'form':form, 'promotion':promotion}
	return render(request, 'accounts/forms/form_promotion_profile.html',  context)


@login_required(login_url='login')
def weeklyPromotion(request):
	promotion1    = Promotion.objects.filter(tag2="Rebate Bonus").last()
	if promotion1:
		promotion1_day	= promotion1.rebate_day
	else:
		promotion1_day = 'none'
	# promotion2    = Promotion.objects.filter(tag2="Ticket")
	date          = timezone.datetime.today()
	date 		  = date.date()

	if promotion1_day == "Sunday" :
		promotion1_day = 6
	elif promotion1_day == "Saturday" :
		promotion1_day = 5
	elif promotion1_day == "Friday" :
		promotion1_day = 4
	elif promotion1_day == "Thursday" :
		promotion1_day = 3
	elif promotion1_day == "Wednesday" :
		promotion1_day = 2
	elif promotion1_day == "Tuesday" :
		promotion1_day = 1
	else:
		promotion1_day = 0
	promotion1_start_week     = date - timedelta(date.weekday()) + timedelta(promotion1_day)
	# promotion1_start_week     = promotion1_start_week.date()
	promotion1_end_week       = promotion1_start_week + timedelta(7)
	promotion1_prv_start_week = promotion1_start_week - timedelta(7)
	return promotion1,promotion1_start_week,promotion1_end_week,promotion1_prv_start_week


#* promotion end

# Games
# @login_required(login_url='login')
def game_on_all_pages(request):
    return {'games': Game.objects.all().order_by("id")}


@login_required(login_url='login')
def manage_game(request):
	games 	= Game.objects.all().order_by("id")
	context = {'games':games}
	return render(request, 'accounts/manage/manage_game.html',  context)


@login_required(login_url='login')
def createGame(request):
	form 	= CreateGameForm()
	if request.method == "POST":
		form = CreateGameForm(request.POST or None)
		if form.is_valid():
			form.save()
			return manage_game(request)

	context = {'form':form}
	return render(request, 'accounts/forms/form_add_game.html',  context)


@login_required(login_url='login')
def editGame(request,pk):
	games        = Game.objects.all().order_by("id")
	game_credits = Transaction.objects.filter(game_backend=pk).order_by("-id")
	paginator    = Paginator(game_credits, 5)
	page         = request.GET.get('page')
	profiles     = paginator.get_page(page)
	if games.filter(id=pk).exists():
		game_this = games.get(id=pk)
		form = CreateGameForm2(instance=game_this)
		if request.method == "POST":
			form = CreateGameForm2(request.POST or None, instance=game_this)
			if form.is_valid():
				form.save()
				context      = {'games':games, 'profiles' : profiles, 'game_this': game_this}
				return render(request, 'accounts/manage/manage_game.html',  context)

		context = {'form':form, 'games':games, 'profiles': profiles,'game_this':game_this}
		return render(request, 'accounts/forms/form_profile_game.html',  context)
	else:
		messages.warning(request, 'System cant find (' + pk + ') please contact admin')

	
	return render(request, 'accounts/manage/manage_game.html',  context)



# Credits
@login_required(login_url='login')
def creditGameAdd(request,pk):
	form      = CreditGameForm()
	game_this = Game.objects.get(id=pk)
	if request.method == "POST":
		form = CreditGameForm(request.POST or None)
		if form.is_valid():
			amount = request.POST.get('amount')
			game_this.credit += float(amount)
			game_this.save()
			form.save()
		else:
			print("error")

	return redirect('edit_game',game_this.id)


@login_required(login_url='login')
def creditGameDeduct(request,pk):
	form      = CreditGameForm()
	game_this = Game.objects.get(id=pk)
	if request.method == "POST":		
		form = CreditGameForm(request.POST or None)
		if form.is_valid():
			amount = request.POST.get('amount')
			game_this.credit -= float(amount)
			amount = " -" + amount
			instance = form.save(commit=False)
			instance.amount = amount
			game_this.save()
			instance.save()

	return redirect('edit_game',game_this.id)


@login_required(login_url='login')
def creditGameWeekly(request,pk,amount):
	form      = CreditWeeklyForm()
	game_this = Game.objects.get(id=pk)
	if request.method == "POST":
		form = CreditWeeklyForm(request.POST or None)
		if form.is_valid():
			# amount = request.POST.get('amount')
			game_this.credit -= float(amount)
			game_this.save()
			form.save()
			# form.fields['action_approve'] = timezone.now()
			# form.action_approve = now()
		else:
			print("error")

	return redirect('home')


@login_required(login_url='login')
def creditGameticket(request,pk):
	# form      = CreditGameForm()
	# game_this = Game.objects.get(id=pk)
	# if request.method == "POST":
	# 	form = CreditGameForm(request.POST or None)
	# 	if form.is_valid():
	# 		amount = request.POST.get('amount')
	# 		game_this.credit += float(amount)
	# 		game_this.save()
	# 		form.save()
	# 	else:
	# 		print("error")

	# return redirect('edit_game',game_this.id)
	return redirect('home')
#* Manage Create Edit



#! Report
@login_required(login_url='login')
def report_sale(request):
	referrals              = Referral.objects.all().order_by("id")
	# customer_ref           = Customer.objects.all()
	transactions           = Transaction.objects.all().exclude(tag="Add_Credit").exclude(tag="Deduct_Credit").order_by('-id')
	paginator              = Paginator(transactions, 10)
	page                   = request.GET.get('page')
	profiles               = paginator.get_page(page)
	today                  = timezone.datetime.today()
	timeNow                = timezone.datetime.now()
	yesterday              = timeNow - timedelta(days=1)
# yesterday2             = yesterday - timedelta(days=1)
	form                   = DateRangeForm()
	date1                  = timeNow.date()
	date2                  = today.now()
	date3                  = date1 - timedelta(days=1)
	date3 				   = timezone.datetime.now() - timedelta(1)
	date3 				   = timezone.datetime.strftime(date3, '%Y-%m-%d')

	customer_ref           = Customer.objects.filter(date_created__gt = date1, date_created__lt = date2)
	todays_customer_report = Customer.objects.filter(date_created__gt = date1, date_created__lt = date2).count()
	transactions           = transactions.filter(date_created__gt = date1, date_created__lt = date2).filter(status="Approved")
	todays_deposit_report  = transactions.filter(customer__date_created__gt = date1, customer__date_created__lt = date2).filter(date_created__gt = date1, date_created__lt = date2).filter(tag="Deposit").order_by('customer').distinct('customer').count()
	transactions_ref       = transactions.filter(customer__date_created__gt = date1, customer__date_created__lt = date2).filter(tag="Deposit").order_by('customer').distinct('customer')
	new_user_transactions  = transactions.filter(customer__date_created__gt = date1, customer__date_created__lt = date2).filter(tag="Deposit").order_by('customer').distinct('customer')
	old_user_transactions  = transactions.filter(customer__date_created__lt = date3).filter(tag="Deposit").order_by('customer').distinct('customer')
	gameAll                = Game.objects.all().count()
	game_list              = {}
	
	
	if request.method == "POST" :
	   form                   = DateRangeForm(request.POST or None)
	   date1                  = request.POST.get("start_date")
	   date2                  = request.POST.get("end_date")
	   date2                  = datetime.strptime(date2 + ' 23:59:59', "%Y-%m-%d %H:%M:%S")
	   date3                  = datetime.strptime(date1 + ' 00:00:00', "%Y-%m-%d %H:%M:%S")
	   date4                  = date3 - timedelta(days=1)
	   customer_ref           = Customer.objects.filter(date_created__gt = date1, date_created__lt = date2)
	   todays_customer_report = Customer.objects.filter(date_created__gt = date1, date_created__lt = date2).count()
	   transactions           = Transaction.objects.all().exclude(tag="Add_Credit").exclude(tag="Deduct_Credit").order_by('-id')
	   transactions           = transactions.filter(date_created__gt = date1, date_created__lt = date2).filter(status="Approved")
	   todays_deposit_report  = transactions.filter(tag="Deposit").filter(customer__date_created__gt = date1, customer__date_created__lt = date2).filter(date_created__gt = F('customer__date_created'), date_created__lt = F('customer__date_created') + timedelta(1)).order_by('customer').distinct('customer').count()
	   transactions_ref       = transactions.filter(tag="Deposit").filter(customer__date_created__gt = date1, customer__date_created__lt = date2).filter(date_created__gt = F('customer__date_created'), date_created__lt = F('customer__date_created') + timedelta(1)).order_by('customer').distinct('customer')
	   old_user_transactions  = transactions.filter(customer__date_created__lt = date3).filter(tag="Deposit").order_by('customer').distinct('customer')

	   #    todays_deposit_report_trs    = transactions.filter(tag="Deposit").filter(customer__date_created__gt = date1, customer__date_created__lt = date2).filter(date_created__gt = F('customer__date_created'), date_created__lt = F('customer__date_created') + timedelta(1))
	   paginator              = Paginator(transactions, 10)
	   page                   = request.GET.get('page')
	   profiles               = paginator.get_page(page)
		


	deposits              = transactions.filter(tag="Deposit")
	deposits_amount       = transactions.filter(tag="Deposit").aggregate(Sum('amount'))
	deposits_amount_promo = transactions.filter(tag="Deposit").aggregate(Sum('amount_promo'))
	if deposits_amount["amount__sum"] is None:
		deposits_amount = 0
	else:
		deposits_amount = deposits_amount["amount__sum"]
	if deposits_amount_promo["amount_promo__sum"] is None:
		deposits_amount_promo = 0
	else:
		deposits_amount_promo = deposits_amount_promo["amount_promo__sum"]

	# Void Credit	= 0

	deposit_free              = transactions.filter(tag="Free")
	deposit_free_amount       = transactions.filter(tag="Free").aggregate(Sum('amount'))
	if deposit_free_amount["amount__sum"] is None:
		deposit_free_amount = 0
	else:
		deposit_free_amount = deposit_free_amount["amount__sum"]


	withdrawals               = transactions.filter(tag="Withdrawal")
	withdrawals_amount        = transactions.filter(tag="Withdrawal").aggregate(Sum('amount'))
	if withdrawals_amount["amount__sum"] is None:
		withdrawals_amount = 0
	else:
		withdrawals_amount = withdrawals_amount["amount__sum"]
	transfers             = transactions.filter(tag="Transfer")


	gross_total			  = deposits_amount - withdrawals_amount
	gameAll = gameAll + 1
	gg	= 1

	while gg < gameAll :
		if Game.objects.filter(id=gg).exists():
			if gg in game_list:
				pass
			else:
				game_list[gg] = []
			game_hold  = Game.objects.filter(id=gg).values_list('name', flat=True)
			game_name  = Game.objects.get(id=gg)
			name_name1 = game_name.name
			game_list[gg] += game_hold	#game name
			trans1     = transactions.filter(tag="Deposit").filter(game__game_name=gg).aggregate(Sum('amount')).get('amount__sum')
			if trans1 == None:
				trans1 = 0
			game_list[gg] += [trans1]
			trans2     = transactions.filter(tag="Withdrawal").filter(game__game_name=gg).aggregate(Sum('amount')).get('amount__sum')
			if trans2 == None:
				trans2 = 0
			game_list[gg] += [trans2]
			trans3     = transactions.filter(tag="Transfer").filter(game__game_name=gg).aggregate(Sum('amount')).get('amount__sum')
			if trans3 == None:
				trans3 = 0
			game_list[gg] += [trans3]
			total = 0
			total += trans1
			total -= trans2
			total -= trans3
			game_list[gg] += [total]
			gg+=1
		else:
			gg+=1
			gameAll += 1
	# print(game_list)
	
	# game            = transactions.filter(game=)	

	# match_queryset.filter(start__gte=d.date(), start__lt=d.date()+timedelta(days=1))
	
	context = {'referrals':referrals, 'form':form, 'timeNow': timeNow, 'yesterday': yesterday, "transactions": transactions,
	"deposits": deposits,"withdrawals": withdrawals,"transfers": transfers,
	"deposits_amount": deposits_amount,"withdrawals": withdrawals,'withdrawals_amount':withdrawals_amount,
	"deposit_free_amount": deposit_free_amount,"deposit_free": deposit_free,
	"game_list": game_list,"profiles": profiles,'deposits_amount_promo':deposits_amount_promo,
	'new_user_transactions':new_user_transactions,'old_user_transactions':old_user_transactions,
	'customer_ref':customer_ref,'transactions_ref':transactions_ref,'todays_deposit_report':todays_deposit_report,
	'gross_total':gross_total,"date1":date1,"date2":date2,'todays_customer_report':todays_customer_report,
	}
	return render(request, 'accounts/report/report_sale.html',  context)


@login_required(login_url='login')
def report_transaction(request):
	banks              = Bank.objects.all().order_by("id")
	transaction        = Transaction.objects.all().order_by('id')
	today              = timezone.datetime.today()
	timeNow            = timezone.datetime.now()
	yesterday          = timeNow - timedelta(days=1)
	form               = DateRangeForm()
	date1              = timeNow.date()
	date2              = timeNow.now()
	transaction_d      = transaction.filter(tag="Deposit").filter(status="Approved").filter(date_created__gt = date1, date_created__lt = date2)
	# deposits_amounts   = transaction_d.aggregate(Sum('amount'))
	transaction_w      = transaction.filter(tag="Withdrawal").filter(status="Approved").filter(date_created__gt = date1, date_created__lt = date2)
	# withdrawals_amount = transaction_w.aggregate(Sum('amount'))

	
	if request.method == "POST":
		form  = DateRangeForm(request.POST or None)
		date1 = request.POST.get("start_date")
		date2 = request.POST.get("end_date")
		date2 = datetime.strptime(date2 + ' 23:59:59', "%Y-%m-%d %H:%M:%S")
		transaction_d = transaction.filter(tag="Deposit").filter(status="Approved").filter(date_created__gt = date1, date_created__lt = date2)
		transaction_w = transaction.filter(tag="Withdrawal").filter(status="Approved").filter(date_created__gt = date1, date_created__lt = date2)

	deposits_amounts    = []
	withdrawals_amounts  = []
	for i in range(banks.count()):
		deposits_amount = transaction_d.filter(bank=i).aggregate(Sum('amount'))
		if deposits_amount["amount__sum"] is None:
			deposits_amount = 0
		else:
			deposits_amount = deposits_amount["amount__sum"]
		# deposits_amounts[i] =[]	
		# deposits_amounts[i] += str(deposits_amount)
		deposits_amounts.append(deposits_amount)
		withdrawals_amount = transaction_w.filter(bank=i).aggregate(Sum('amount'))
		if withdrawals_amount["amount__sum"] is None:
			withdrawals_amount = 0
		else:
			withdrawals_amount = withdrawals_amount["amount__sum"]
		# withdrawals_amounts[i] = []
		# withdrawals_amounts[i] += str(withdrawals_amount)
		withdrawals_amounts.append(withdrawals_amount)


	context = {'banks':banks, 'transaction_d':transaction_d, 'transaction_w':transaction_w,
		'date1':date1,'date2':date2,'deposits_amounts':deposits_amounts,'withdrawals_amounts':withdrawals_amounts,
	}
	return render(request, 'accounts/report/report_transaction.html',  context)

#* Report End




@login_required(login_url='login')
def follow_ups(request):
	context = {}
	return render(request, 'accounts/user/follow_ups.html',  context)


@login_required(login_url='login')
def list_4d(request):
	context = {}
	return render(request, 'accounts/transaction/list_4d.html',  context)


@login_required(login_url='login')
def list_weekly(request):
	context = {}
	return render(request, 'accounts/transaction/list_weekly.html',  context)


@login_required(login_url='login')
def blacklist_bank(request):
	context = {}
	return render(request, 'accounts/user/blacklist_bank.html',  context)


@login_required(login_url='login')
def manage_employee(request):
	users = User.objects.all().order_by("id")
	context = {"users":users}
	return render(request, 'accounts/employee/manage_employee.html',  context)


@login_required(login_url='login')
def manage_position(request):
	user = request.user
	logger.warning("User.ID=" + str(user.id))

	if request.method == 'POST':
		positions = request.POST.getlist('positions[]')

		items = []
		if positions and len(positions) > 0:
			for position_id in positions:
				items.append(User_Position(user_id=user.id, position_id=position_id))

		User_Position.objects.bulk_create(items)

	position_group = Positions.objects.values('group').annotate(Count("id"))
	positions = Positions.objects.all().order_by("id")	
	user_positions = User_Position.objects.filter(user_id=user.id).only("position_id")
	
	user_positions = map(lambda x: x.position_id, list(user_positions))
	user_positions = list(user_positions)
	
	# positions = list(positions)
	# for pos in positions:
	# 	logger.warning(pos.id)
	# 	matches = any(x for x in user_positions if pos.id == x.position_id)
	# 	logger.warning(matches)
	# 	if matches:
	# 		pos.state = 1

	logger.warning(user_positions)
	context = {
		"position_group": position_group,
		"positions": positions, 
		"user_positions": user_positions
	}
	return render(request, 'accounts/employee/manage_position.html',  context)
	

@login_required(login_url='login')
def action_logs(request):
	context = {}
	return render(request, 'accounts/employee/action_logs.html',  context)


@login_required(login_url='login')
def sms_not_include(request):
	context = {}
	return render(request, 'accounts/manage/sms_not_include.html',  context)


def sms(request):
	gatewayForm = CreateSMSGatewayForm()
	gateway = gatewayForm.save(commit=False)
	gateway.name = 'sms_received'
	gateway.save()
	context = {}
	return render(request, 'accounts/manage/sms_not_include.html',  context)







	



















		





