from django import template
from datetime import datetime, date, timedelta
from django.utils import timezone
from ..models import * 	#all models
from ..signals import *

register = template.Library()

def re_m_deposit(text):
	customer1      = Transaction.objects.get(id=text)
	successMessage = SuccessMessage.objects.all().last()
	if int(customer1.withdrawal_limit_max) > 0:
		replace_to	= "Game : " + str(customer1.game.game_name) + "\nUsername : " + str(customer1.game.username) + "\nTopup: " + str(float(customer1.amount) + float(customer1.amount_free)) + "\nDapat: " + str(float(customer1.amount) + float(customer1.amount_promo) + float(customer1.amount_free)) + "\nMin Cuci: " + str(customer1.withdrawal_limit_min) + "\nMax Cuci: " + str(customer1.withdrawal_limit_max) + "\n\n" + str(customer1.promotion)
	else:
		replace_to	= "Game : " + str(customer1.game.game_name) + "\nUsername : " + str(customer1.game.username) + "\nTopup: " + str(float(customer1.amount) + float(customer1.amount_free)) + "\nDapat: " + str(float(customer1.amount) + float(customer1.amount_promo) + float(customer1.amount_free)) + "\nMin Cuci: " + str(customer1.withdrawal_limit_min) + "\n\n" + str(customer1.promotion)
	successMessage = successMessage.m_deposit.replace('[*VAR1*]',replace_to)
	return successMessage


def re_c_deposit(text):
	customer1      = Transaction.objects.get(id=text)
	successMessage = SuccessMessage.objects.all().last()
	if int(customer1.withdrawal_limit_max) > 0:
		replace_to	= "Game : " + str(customer1.game.game_name) + "\nUsername : " + str(customer1.game.username) + "\n充值: " + str(customer1.amount) + "\n得到: " + str(float(customer1.amount) + float(customer1.amount_promo)) + "\n最低提款: " + str(customer1.withdrawal_limit_min) + "\nMax Cuci: " + str(customer1.withdrawal_limit_max) + "\n\n" + str(customer1.promotion)
	else:
		replace_to	= "Game : " + str(customer1.game.game_name) + "\nUsername : " + str(customer1.game.username) + "\n充值: " + str(customer1.amount) + "\n得到: " + str(float(customer1.amount) + float(customer1.amount_promo)) + "\n最低提款: " + str(customer1.withdrawal_limit_min) + "\n\n" + str(customer1.promotion)
	successMessage = successMessage.c_deposit.replace('[*VAR1*]',replace_to)
	return successMessage

def re_e_deposit(text):
	customer1      = Transaction.objects.get(id=text)
	successMessage = SuccessMessage.objects.all().last()
	if int(customer1.withdrawal_limit_max) > 0:
		replace_to	= "Game : " + str(customer1.game.game_name) + "\nUsername : " + str(customer1.game.username) + "\nDeposit: " + str(customer1.amount) + "\nGet: " + str(float(customer1.amount) + float(customer1.amount_promo)) + "\nMin Cuci: " + str(customer1.withdrawal_limit_min) + "\nMax Cuci: " + str(customer1.withdrawal_limit_max) + "\n\n" + str(customer1.promotion)
	else:
		replace_to	= "Game : " + str(customer1.game.game_name) + "\nUsername : " + str(customer1.game.username) + "\nDeposit: " + str(customer1.amount) + "\nGet: " + str(float(customer1.amount) + float(customer1.amount_promo)) + "\nMin Cuci: " + str(customer1.withdrawal_limit_min) + "\n\n" + str(customer1.promotion)
	successMessage = successMessage.e_deposit.replace('[*VAR1*]',replace_to)
	return successMessage



def re_m_withdrawal(text):
	customer1      = Transaction.objects.get(id=text)
	successMessage = SuccessMessage.objects.all().last()
	if customer1.customer.bank_name:
		replace_to	= "Amount : " + str(customer1.amount) + "\nBank : " + str(customer1.customer.bank_name) + "\n" + str(customer1.customer.account_name) + "\n" + str(customer1.customer.account_number)
	else :
		replace_to	= "Amount : " + str(customer1.amount) + "\nCustomer Bank Have Not Setup Yet"
	successMessage = successMessage.m_withdrawal.replace('[*VAR1*]',replace_to)
	return successMessage

def re_c_withdrawal(text):
	customer1      = Transaction.objects.get(id=text)
	successMessage = SuccessMessage.objects.all().last()
	if customer1.customer.bank_name:
		replace_to	= "总额 : " + str(customer1.amount) + "\n银行 : " + str(customer1.customer.bank_name) + "\n" + str(customer1.customer.account_name) + "\n" + str(customer1.customer.account_number)
	else :
		replace_to	= "总额 : " + str(customer1.amount) + "\nCustomer Bank Have Not Setup Yet"
	successMessage = successMessage.c_withdrawal.replace('[*VAR1*]',replace_to)
	return successMessage

def re_e_withdrawal(text):
	customer1      = Transaction.objects.get(id=text)
	successMessage = SuccessMessage.objects.all().last()
	if customer1.customer.bank_name:
		replace_to	= "Amount : " + str(customer1.amount) + "\nBank : " + str(customer1.customer.bank_name) + "\n" + str(customer1.customer.account_name) + "\n" + str(customer1.customer.account_number)
	else :
		replace_to	= "Amount : " + str(customer1.amount) + "\nCustomer Bank Have Not Setup Yet"
	successMessage = successMessage.e_withdrawal.replace('[*VAR1*]',replace_to)
	return successMessage



def re_m_transfer(text):
	customer1      = Transaction.objects.get(id=text)
	successMessage = SuccessMessage.objects.all().last()
	if customer1.game.game_name and customer1.game2.game_name:
		replace_to	= "Dari Game: " + str(customer1.game.game_name) + "\nGame ID: " + str(customer1.game.username)
		replace_to1	= "\nKe Game: " + str(customer1.game2.game_name) + "\nGame ID: " + str(customer1.game2.username) + "\n\nTransfer:" + str(customer1.amount)
	else :
		replace_to	= "Please Setup Game1 and Game2"
	successMessage = successMessage.m_transfer.replace('[*VAR1*]',replace_to).replace('[*VAR2*]',replace_to1)
	return successMessage

def re_c_transfer(text):
	customer1      = Transaction.objects.get(id=text)
	successMessage = SuccessMessage.objects.all().last()
	if customer1.game.game_name and customer1.game2.game_name:
		replace_to	= "Dari Game: " + str(customer1.game.game_name) + "\nGame ID: " + str(customer1.game.username)
		replace_to1	= "\nKe Game: " + str(customer1.game2.game_name) + "\nGame ID: " + str(customer1.game2.username) + "\n\nTransfer:" + str(customer1.amount)
	else :
		replace_to	= "Please Setup Game1 and Game2"
	successMessage = successMessage.c_transfer.replace('[*VAR1*]',replace_to).replace('[*VAR2*]',replace_to1)
	return successMessage

def re_e_transfer(text):
	customer1      = Transaction.objects.get(id=text)
	successMessage = SuccessMessage.objects.all().last()
	if customer1.game.game_name and customer1.game2.game_name:
		replace_to	= "Dari Game: " + str(customer1.game.game_name) + "\nGame ID: " + str(customer1.game.username)
		replace_to1	= "\n\nKe Game: " + str(customer1.game2.game_name) + "\nGame ID: " + str(customer1.game2.username) + "\n\nTransfer:" + str(customer1.amount)
	else :
		replace_to	= "Please Setup Game1 and Game2"
	successMessage = successMessage.e_transfer.replace('[*VAR1*]',replace_to).replace('[*VAR2*]',replace_to1)
	return successMessage





def re_m_withdrawal_verify_bank(text):
	customer1      = Transaction.objects.get(id=text)
	successMessage = SuccessMessage.objects.all().last()
	replace_to	= str(customer1.customer.bank_name) + "\n" + str(customer1.customer.account_name) + "\n" + str(customer1.customer.account_number)
	successMessage = successMessage.m_withdrawal_verify_bank.replace('[*VAR1*]',replace_to)
	return successMessage

def re_c_withdrawal_verify_bank(text):
	customer1      = Transaction.objects.get(id=text)
	successMessage = SuccessMessage.objects.all().last()
	replace_to	=  str(customer1.customer.bank_name) + "\n" + str(customer1.customer.account_name) + "\n" + str(customer1.customer.account_number)
	successMessage = successMessage.c_withdrawal_verify_bank.replace('[*VAR1*]',replace_to)
	return successMessage

def re_e_withdrawal_verify_bank(text):
	customer1      = Transaction.objects.get(id=text)
	successMessage = SuccessMessage.objects.all().last()
	replace_to	=  str(customer1.customer.bank_name) + "\n" + str(customer1.customer.account_name) + "\n" + str(customer1.customer.account_number)
	successMessage = successMessage.e_withdrawal_verify_bank.replace('[*VAR1*]',replace_to)
	return successMessage








def re_m_newgameid(text):
	customer1      = CustomerGame.objects.get(id=text)
	successMessage = SuccessMessage.objects.all().last()
	replace_to	= "Game : " + str(customer1.game_name) + "\nUsername : " + str(customer1.username) + "\nPassword : " + str(customer1.password) + "\nDownload: " + str(customer1.game_name.url)
	successMessage = successMessage.m_newgameid.replace('[*VAR1*]',replace_to)
	return successMessage

def re_c_newgameid(text):
	customer1      = CustomerGame.objects.get(id=text)
	successMessage = SuccessMessage.objects.all().last()
	replace_to	= "Game : " + str(customer1.game_name) + "\nUsername : " + str(customer1.username) + "\nPassword : " + str(customer1.password) + "\nDownload: " + str(customer1.game_name.url)
	successMessage = successMessage.c_newgameid.replace('[*VAR1*]',replace_to)
	return successMessage

def re_e_newgameid(text):
	customer1      = CustomerGame.objects.get(id=text)
	successMessage = SuccessMessage.objects.all().last()
	replace_to	= "Game : " + str(customer1_name) + "\nUsername : " + str(customer1.username) + "\nPassword : " + str(customer1.game.password) + "\nDownload: " + str(customer1.game_name.url)
	successMessage = successMessage.e_newgameid.replace('[*VAR1*]',replace_to)
	return successMessage







#btn for game link
def btn_setscore(text):
	game_id    = CustomerGame.objects.get(id=text)
	successMessage = game_id.game_name.link_setscore
	if successMessage:
		replace_to     = str(game_id.username)
		successMessage = successMessage.replace('[*USERID*]',replace_to)
	else:
		successMessage = ""
	return successMessage
def btn_scorelog(text):
	game_id    = CustomerGame.objects.get(id=text)
	successMessage = game_id.game_name.link_scorelog
	if successMessage:
		replace_to     = str(game_id.username)
		successMessage = successMessage.replace('[*USERID*]',replace_to)
	else:
		successMessage = ""
	return successMessage
def btn_gamelog(text):
	game_id    = CustomerGame.objects.get(id=text)
	successMessage = game_id.game_name.link_gamelog
	if successMessage:
		replace_to     = str(game_id.username)
		successMessage = successMessage.replace('[*USERID*]',replace_to)
	else:
		successMessage = ""
	return successMessage
def btn_edit(text):
	game_id    = CustomerGame.objects.get(id=text)
	successMessage = game_id.game_name.link_resetpass
	if successMessage:
		replace_to     = str(game_id.username)
		successMessage = successMessage.replace('[*USERID*]',replace_to)
	else:
		successMessage = ""
	return successMessage





def add(a, b):
    return a+b






today_date = timezone.datetime.now().strftime("$Y%m%d")
if True: #int(today_date) < int(Regireg()):
	register.filter('add', add)
	register.filter('re_m_deposit', re_m_deposit)
	register.filter('re_e_deposit', re_e_deposit)
	register.filter('re_c_deposit', re_c_deposit)
	register.filter('re_m_withdrawal', re_m_withdrawal)
	register.filter('re_e_withdrawal', re_e_withdrawal)
	register.filter('re_c_withdrawal', re_c_withdrawal)
	register.filter('re_m_newgameid', re_m_newgameid)
	register.filter('re_e_newgameid', re_e_newgameid)
	register.filter('re_c_newgameid', re_c_newgameid)
	register.filter('re_m_withdrawal_verify_bank', re_m_withdrawal_verify_bank)
	register.filter('re_e_withdrawal_verify_bank', re_e_withdrawal_verify_bank)
	register.filter('re_c_withdrawal_verify_bank', re_c_withdrawal_verify_bank)
	register.filter('re_m_transfer', re_m_transfer)
	register.filter('re_e_transfer', re_e_transfer)
	register.filter('re_c_transfer', re_c_transfer)
	register.filter('btn_setscore', btn_setscore)
	register.filter('btn_scorelog', btn_scorelog)
	register.filter('btn_gamelog', btn_gamelog)
	register.filter('btn_edit', btn_edit)
