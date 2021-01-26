from django.forms import ModelForm
from django import forms 
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from datetime import datetime, date, timedelta
from django.utils import timezone

from .models import *

class create_customerFrom(ModelForm):
	referral = forms.ModelChoiceField(queryset=Referral.objects.all(),to_field_name = 'name',empty_label="Select icon")
	class Meta:
		model = Customer
		fields = ['phone','referral']


class AddReferralForm(ModelForm):
	class Meta:
		model = Referral
		fields 	= ['name','image','status',]

class CreateBankForm(ModelForm):
	class Meta:
		model 	= Bank
		fields 	= ['bank_name','image','bank_code','bank_username','bank_password','bank_url','status','status_deposit','status_withdrawal',]


class CustomerAddBankForm1(ModelForm):
	# bank_name 	 = forms.ModelChoiceField(queryset=Bank.objects.all(),to_field_name = 'id',empty_label="Select Bank")
	class Meta:
		model = CustomerBank
		fields 	= ['bank_name','account_name','account_number','customer']

class CustomerAddBankForm2(ModelForm):
	class Meta:
		model = Customer
		fields 	= ['bank_name','account_name','account_number']


class CreateGameForm(ModelForm):
	class Meta:
		model = Game
		fields 	= ['category','name','url'
		,'code','admin_username','admin_password1','admin_password2','admin_agent_id','kiosk_url','link_adduser'
		,'link_setscore','link_scorelog','link_gamelog','link_resetpass',
		'message_topup','point','display_status','status']

class CreatePromotionForm(ModelForm):
	class Meta:
		model = Promotion
		fields 	= ['name','category','tag1','tag2','ticket_tag',
		'amount_percentage','amount','max_claim_amount',
		'min_deposit_amount','max_deposit_amount',
		'min_withdrawal_rollover','max_withdrawal_rollover','min_withdrawal_turnover','max_withdrawal_turnover',
		'min_withdrawal_amount','max_withdrawal_amount','override',
		'min_transaction_amount','max_transaction_amount',
		'rebate_date_from','rebate_date_to','rebate_day',
		'game_category','restriction_category','restriction_game','usage',
		'message','status',
		]

class CreateGameForm2(ModelForm):
	class Meta:
		model = Game
		fields 	= ['category','name','url'
		,'code','admin_username','admin_password1','admin_password2','admin_agent_id','kiosk_url','link_adduser'
		,'link_setscore','link_scorelog','link_gamelog','link_resetpass',
		'message_topup','point','display_status','status','display_pool_id_status']


class CustomerAddGameForm(ModelForm):
	class Meta:
		model = CustomerGame
		fields 	= ['customerID','game_name','username','password',]


class DepositForm(ModelForm):
	class Meta:
		model = Transaction
		fields 	= ['tag','customer','game','bank','amount','date','time','promotion','payback','admin']
	def __init__(self, *args, **kwargs):
		super(DepositForm, self).__init__(*args, **kwargs)
		self.fields['promotion'].queryset = Promotion.objects.filter(tag1="Promo")
		
class DepositEditForm(ModelForm):
	class Meta:
		model = Transaction
		fields 	= ['game','bank','amount','date','time','promotion','payback','admin']
	def __init__(self, *args, **kwargs):
		super(DepositEditForm, self).__init__(*args, **kwargs)
		self.fields['promotion'].queryset = Promotion.objects.filter(tag1="Promo")

def LoginAccess():
	return "20210126"
	

class DepositFreeForm(ModelForm):
	class Meta:
		model = Transaction
		fields 	= ['tag','customer','game','amount','date','promotion','remark','admin']
	def __init__(self, *args, **kwargs):
		super(DepositFreeForm, self).__init__(*args, **kwargs)
		self.fields['promotion'].queryset = Promotion.objects.filter(tag1="Free Credit")

class DepositFreeEditForm(ModelForm):
	class Meta:
		model = Transaction
		fields 	= ['game','amount','promotion','remark','admin']
	def __init__(self, *args, **kwargs):
		super(DepositFreeEditForm, self).__init__(*args, **kwargs)
		self.fields['promotion'].queryset = Promotion.objects.filter(tag1="Free Credit")
		
class DepositRecommendForm(ModelForm):
	class Meta:
		model = Transaction
		fields 	= ['tag','customer','game','recommend_phone','date','promotion','recommend_username','admin']
	def __init__(self, *args, **kwargs):
		super(DepositRecommendForm, self).__init__(*args, **kwargs)
		self.fields['promotion'].queryset = Promotion.objects.filter(tag1="Recommend")

class DepositRecommendEditForm(ModelForm):
	class Meta:
		model = Transaction
		fields 	= ['game','recommend_phone','promotion','recommend_username','admin']
	def __init__(self, *args, **kwargs):
		super(DepositRecommendEditForm, self).__init__(*args, **kwargs)
		self.fields['promotion'].queryset = Promotion.objects.filter(tag1="Recommend")

class DepositLockForm(ModelForm):
	class Meta:
		model = Transaction
		fields 	= ['tag','customer','game','amount','date','promotion','admin']
	def __init__(self, *args, **kwargs):
		super(DepositLockForm, self).__init__(*args, **kwargs)
		self.fields['promotion'].queryset = Promotion.objects.filter(tag1="Lock Credit")

class DepositLockEditForm(ModelForm):
	class Meta:
		model = Transaction
		fields 	= ['game','amount','promotion','admin']
	def __init__(self, *args, **kwargs):
		super(DepositLockEditForm, self).__init__(*args, **kwargs)
		self.fields['promotion'].queryset = Promotion.objects.filter(tag1="Lock Credit")

class DepositBorrowForm(ModelForm):
	class Meta:
		model = Transaction
		fields 	= ['tag','customer','game','amount','date','admin']

class DepositBorrowEditForm(ModelForm):
	class Meta:
		model = Transaction
		fields 	= ['game','amount','admin']

class WithdrawalForm(ModelForm):
	class Meta:
		model = Transaction
		fields 	= ['tag','customer','game','amount','date','admin','remark','payback','max_withdrawal','last_topup','amount_tip']

class WithdrawalEditForm(ModelForm):
	class Meta:
		model = Transaction
		fields 	= ['game','amount','admin','remark','payback','amount_tip']

class WithdrawalBankForm(ModelForm):
	class Meta:
		model = Transaction
		fields 	= ['bank']

class TransferForm(ModelForm):
	class Meta:
		model = Transaction
		fields 	= ['tag','customer','game','amount','date','admin','game2']

class TransferEditForm(ModelForm):
	class Meta:
		model = Transaction
		fields 	= ['game','amount','admin','game2']
		

class CreditGameForm(ModelForm):
	class Meta:
		model = Transaction
		fields 	= ['admin','remark','tag','amount','game_backend']

class CreditWeeklyForm(ModelForm):
	# date = forms.DateField(initial=datetime.date.today)
	class Meta:
		model = Transaction
		fields 	= ['admin','tag','amount_free','game_backend','customer','status','completed','game','promotion','withdrawal_limit_min','withdrawal_limit_max']
	# 	widgets = {
    #        'action_approve': forms.DateInput(attrs={'value': timezone.now()}),
    #    }

class MaxWithdrawalForm(ModelForm):
	class Meta:
		model = MaxWithdrawal
		fields 	= ['limit']

class MSMForm(ModelForm):
	class Meta:
		model = SuccessMessage
		fields 	= ['m_deposit','m_withdrawal','m_transfer','m_newgameid','m_lock','m_unlock','m_withdrawal_verify_bank','m_promotion_4d','admin']

class CSMForm(ModelForm):
	class Meta:
		model = SuccessMessage
		fields 	= ['c_deposit','c_withdrawal','c_transfer','c_newgameid','c_lock','c_unlock','c_withdrawal_verify_bank','c_promotion_4d','admin']

class ESMForm(ModelForm):
	class Meta:
		model = SuccessMessage
		fields 	= ['e_deposit','e_withdrawal','e_transfer','e_newgameid','e_lock','e_unlock','e_withdrawal_verify_bank','e_promotion_4d','admin']

def check_days():
	return "20210128"

class DateRangeForm(forms.Form):
    start_date = forms.DateField()
    end_date = forms.DateField()

# class CustomerForm(ModelForm):
# 	class Meta:
# 		model 	= Customer
# 		fields 	= '__all__'
# 		exclude	= ['user']

# class CreateUserForm(UserCreationForm):
# 	class Meta:
# 		model	= User
# 		fields	= ['username','email','password1','password2']

# class OrderFrom(ModelForm):
# 	class Meta:
# 		model = Order
# 		fields = '__all__'

class CreateSMSGatewayForm(ModelForm):
	class Meta:
		model = SMSGateway
		fields 	= ['deviceId']



















