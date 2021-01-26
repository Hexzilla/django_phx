from django.db import models
from django.contrib.auth.models import User, Group
from django.core.validators import MinLengthValidator, int_list_validator

# Create your models here.


class Game(models.Model):	#add_game
	CATEGORY = {
		('Slot','Slot'),
		('Casino','Casino'),
		('Sports','Sports'),
		('Fish','Fish'),
		('7/11','7/11'),
	}

	STATUS =	(
		('Active','Active'),
		('Inactive','Inactive'),
	)

	name                   = models.CharField(max_length=254, null=False, blank=False, unique=True)
	category               = models.CharField(max_length=200, null=True, blank=True,choices=CATEGORY)
	url                    = models.CharField(max_length=254, null=True, blank=True)
	code                   = models.CharField(max_length=254, null=True, blank=True)
	admin_username         = models.CharField(max_length=254, null=True, blank=True)
	admin_password1        = models.CharField(max_length=254, null=True, blank=True)
	admin_password2        = models.CharField(max_length=254, null=True, blank=True)
	admin_agent_id         = models.CharField(max_length=254, null=True, blank=True)
	kiosk_url              = models.CharField(max_length=254, null=True, blank=True)
	link_adduser           = models.CharField(max_length=254, null=True, blank=True)
	link_setscore          = models.CharField(max_length=254, null=True, blank=True)
	link_scorelog          = models.CharField(max_length=254, null=True, blank=True)
	link_gamelog           = models.CharField(max_length=254, null=True, blank=True)
	link_resetpass         = models.CharField(max_length=254, null=True, blank=True)
	message_topup          = models.TextField(max_length=254, null=True, blank=True)
	point                  = models.FloatField(default=0)
	display_status         = models.CharField(max_length=200, null=True, choices=STATUS,default='Active')
	status                 = models.CharField(max_length=200, null=True, choices=STATUS,default='Active')
	display_pool_id_status = models.CharField(max_length=200, null=True, choices=STATUS,default='Active')
	# total credit of the game
	credit	               = models.FloatField(default=0)

	#date & time
	date_created = models.DateTimeField(auto_now_add=True)
	date_updated = models.DateTimeField(auto_now=True)


	def __str__(self):
	 return self.name


class Promotion(models.Model):	#add_game
	CATEGORY = {
		('Slot','Slot'),
		('Casino','Casino'),
		('Sports','Sports'),
		('Fish','Fish'),
		('7/11','7/11'),
	}

	MAIN =	(
		('Main','Main'),
	)

	STATUS =	(
		('Active','Active'),
		('Inactive','Inactive'),
	)

	ONOFF =	(
		('On','On'),
		('Off','Off'),
	)

	DAY =	(
		('Monday','Monday'),
		('Tuesday','Tuesday'),
		('Wednesday','Wednesday'),
		('Thursday','Thursday'),
		('Friday','Friday'),
		('Saturday','Saturday'),
		('Sunday','Sunday'),
	)

	USAGE = {
		('Daily','Daily'),
		('Weekly','Weekly'),
		('Monthly','Monthly'),
		('Yearly','Yearly'),
		('One Time Only','One Time Only'),
		('Unlimited','Unlimited'),
		('Twice a Day','Twice a Day'),
		('Thrice a Day','Thrice a Day'),
	}
	PROMO_TYPE1 = {
		('Promo','Promo'),
		('Free Credit','Free Credit'),
		('Recommend','Recommend'),
		('Void Credit','Void Credit'),
		('Borrow Credit','Borrow Credit'),
		('Lock Credit','Lock Credit'),
		('Withdrawal','Withdrawal'),
	}
	PROMO_TYPE2 = {
		('Rebate Bonus','Rebate Bonus'),
		('No Bonus','No Bonus'),
		('No Bonus Topup','No Bonus (Below Minimum Topup Amount)'),
		('Ticket','Ticket'), #By accumulate    By per ticket   
	}

	TICKET_TAG =	(
		('Accumulate','By Accumulate'),
		('Ticket','By Per Ticket'),
	)

	name                    = models.CharField(max_length=254, null=False,blank=False)
	category                = models.CharField(max_length=200, null=True, blank=True,choices=MAIN)
	tag1                    = models.CharField(max_length=200, null=True, blank=True,choices=PROMO_TYPE1)
	tag2                    = models.CharField(max_length=200, null=True, blank=True,choices=PROMO_TYPE2)
	ticket_tag              = models.CharField(max_length=200, null=True, blank=True,choices=TICKET_TAG)
	amount_percentage       = models.IntegerField(default=0)
	amount                  = models.FloatField(default=0.00)
	max_claim_amount        = models.FloatField(default=0.00)
	min_transaction_amount  = models.FloatField(default=0.00)
	max_transaction_amount  = models.FloatField(default=0.00)
	min_deposit_amount      = models.FloatField(default=0.00)
	max_deposit_amount      = models.FloatField(default=0.00)
	min_withdrawal_rollover = models.FloatField(default=0.00)
	max_withdrawal_rollover = models.FloatField(default=0.00)
	min_withdrawal_turnover = models.FloatField(default=0.00)
	max_withdrawal_turnover = models.FloatField(default=0.00)
	min_withdrawal_amount   = models.FloatField(default=0.00)
	max_withdrawal_amount   = models.FloatField(default=0.00)
	override                = models.CharField(default="Off", max_length=200, null=True, blank=True,choices=ONOFF)
	rebate_date_from        = models.CharField(max_length=254, null=True, blank=True)
	rebate_date_to          = models.CharField(max_length=254, null=True, blank=True)
	rebate_day              = models.CharField(default="Off", max_length=200, null=True, blank=True,choices=DAY)
	game_category           = models.CharField(max_length=200, null=True, blank=True,choices=CATEGORY)
	restriction_category    = models.CharField(max_length=200, null=True, blank=True,choices=CATEGORY)
	restriction_game        = models.ForeignKey(Game, null=True, blank=True, on_delete=models.SET_NULL)
	usage                   = models.CharField(max_length=200, null=True, blank=True,choices=USAGE)
	message                 = models.TextField(max_length=254, null=True, blank=True)
	status                  = models.CharField(max_length=200, null=True, choices=STATUS,default='Active')\

	#date & time
	date_created = models.DateTimeField(auto_now_add=True)
	date_updated = models.DateTimeField(auto_now=True)


	def __str__(self):
	 return self.name


# class CreditRecord(models.Model):
# 	game_name    = models.ForeignKey(Game, on_delete=models.CASCADE, null=False,blank=False)
# 	admin        = models.CharField("Admin" , max_length=254, null=False, blank=False, default='System')
# 	reference_id = models.CharField("RefID" , max_length=254, null=True, blank=True)
# 	reference_no = models.CharField("RefNo" , max_length=254, null=True, blank=True)
# 	remark       = models.TextField("Remark" , max_length=254, null=True, blank=True)
# 	credit_type  = models.CharField(max_length=254, null=False, blank=False, default='System')
# 	amount       = models.FloatField(default=0)
# 	#date & time
# 	date_created = models.DateTimeField('Date Created',auto_now_add=True)
# 	date_updated = models.DateTimeField('Date Updated',auto_now=True)

# 	def __str__(self):
# 	 return "C%08d" % self.id



class Referral(models.Model):	#add_referral_icon
	STATUS =	(
		('Active','Active'),
		('Inactive','Inactive'),
	)

	name   = models.CharField(max_length=254, unique=True, null=False,blank=False)
	image  = models.ImageField(upload_to='referral/', blank=False)
	status = models.CharField("Status", max_length=80, default='Active', choices=STATUS)
	total  = models.IntegerField(default=0, blank=True, null=True)
	#date & time
	date_created = models.DateTimeField(auto_now_add=True)
	date_updated = models.DateTimeField(auto_now=True)

	def __str__(self):
		return self.name


class MaxWithdrawal(models.Model):
	STATUS =	(
		('Active','Active'),
		('Inactive','Inactive'),
	)

	limit        = models.IntegerField(default=3, blank=False, null=False)
	status       = models.CharField("Status", max_length=80, default='Active', choices=STATUS)
	#date & time
	date_created = models.DateTimeField(auto_now_add=True)
	date_updated = models.DateTimeField(auto_now=True)





class Bank(models.Model):	#add_bank
	STATUS =	(
		('Active','Active'),
		('Inactive','Inactive'),
	)

	bank_name         = models.CharField(max_length=200, null=False,blank=False, unique=True)
	bank_code         = models.CharField(max_length=200, null=False,blank=False)
	bank_username     = models.CharField(max_length=200, null=True,blank=True)
	bank_password     = models.CharField(max_length=200, null=True,blank=True)
	bank_url          = models.CharField(max_length=200, null=True,blank=True)
	account_name      = models.CharField(max_length=200, null=True,blank=True)
	account_number    = models.CharField(max_length=30,  null=True,blank=True)
	image             = models.ImageField(upload_to='bank/', blank=False)
	status            = models.CharField("Status", max_length=80, default='Active', choices=STATUS)
	status_deposit    = models.CharField( max_length=80, default='Active', choices=STATUS)
	status_withdrawal = models.CharField( max_length=80, default='Active', choices=STATUS)
	#date & time
	date_created = models.DateTimeField(auto_now_add=True)
	date_updated = models.DateTimeField(auto_now=True)

	def __str__(self):
	 return self.bank_name


class SuccessMessage(models.Model):
	m_deposit                = models.TextField(max_length=5000, null=True, blank=True, default="No Setup Message")
	m_withdrawal             = models.TextField(max_length=5000, null=True, blank=True, default="No Setup Message")
	m_transfer               = models.TextField(max_length=5000, null=True, blank=True, default="No Setup Message")
	m_newgameid              = models.TextField(max_length=5000, null=True, blank=True, default="No Setup Message")
	m_lock                   = models.TextField(max_length=5000, null=True, blank=True, default="No Setup Message")
	m_unlock                 = models.TextField(max_length=5000, null=True, blank=True, default="No Setup Message")
	m_withdrawal_verify_bank = models.TextField(max_length=5000, null=True, blank=True, default="No Setup Message")
	m_promotion_4d           = models.TextField(max_length=5000, null=True, blank=True, default="No Setup Message")

	c_deposit                = models.TextField(max_length=5000, null=True, blank=True, default="No Setup Message")
	c_withdrawal             = models.TextField(max_length=5000, null=True, blank=True, default="No Setup Message")
	c_transfer               = models.TextField(max_length=5000, null=True, blank=True, default="No Setup Message")
	c_newgameid              = models.TextField(max_length=5000, null=True, blank=True, default="No Setup Message")
	c_lock                   = models.TextField(max_length=5000, null=True, blank=True, default="No Setup Message")
	c_unlock                 = models.TextField(max_length=5000, null=True, blank=True, default="No Setup Message")
	c_withdrawal_verify_bank = models.TextField(max_length=5000, null=True, blank=True, default="No Setup Message")
	c_promotion_4d           = models.TextField(max_length=5000, null=True, blank=True, default="No Setup Message")

	e_deposit                = models.TextField(max_length=5000, null=True, blank=True, default="No Setup Message")
	e_withdrawal             = models.TextField(max_length=5000, null=True, blank=True, default="No Setup Message")
	e_transfer               = models.TextField(max_length=5000, null=True, blank=True, default="No Setup Message")
	e_newgameid              = models.TextField(max_length=5000, null=True, blank=True, default="No Setup Message")
	e_lock                   = models.TextField(max_length=5000, null=True, blank=True, default="No Setup Message")
	e_unlock                 = models.TextField(max_length=5000, null=True, blank=True, default="No Setup Message")
	e_withdrawal_verify_bank = models.TextField(max_length=5000, null=True, blank=True, default="No Setup Message")
	e_promotion_4d           = models.TextField(max_length=5000, null=True, blank=True, default="No Setup Message")

	admin 					 = models.CharField(max_length=200, blank=False,null=False)
	#date & time
	date_created 			 = models.DateTimeField(auto_now_add=True)
	date_updated 			 = models.DateTimeField(auto_now=True)

	def __str__(self):
			return "Message%06d" % self.id


class Customer(models.Model):	#Create_Customer

	def showid(self):
		return "PHX%06d" % self.id

	STATUS =	(
		('Active','Active'),
		('Inactive','Inactive'),
	)
	BANS =	(
		('No','No'),
		('Blacklist','Blacklist'),
		('Banned','Banned'),
	)
	LANGUAGE =	(
		('Malay','Malay'),
		('Chinese','Chinese'),
		('English','English'),
	)

	name           = showid
	phone          = models.CharField(max_length=15,validators=[int_list_validator(),MinLengthValidator(9),] , blank=False, unique=True)
	referral       = models.ForeignKey(Referral, on_delete=models.SET_NULL, null=True)
	gander         = models.CharField( max_length=50, null=True, blank=True)
	wechat         = models.CharField( max_length=254, null=True, blank=True)
	telegram       = models.CharField( max_length=254, null=True, blank=True)
	email          = models.EmailField(default="NoEmail@gmail.com",max_length=254, null=True, blank=True)
	status         = models.CharField(max_length=80, default='Active', choices=STATUS)
	blacklist      = models.CharField( max_length=80, default='No', choices=BANS)
	language       = models.CharField( max_length=80, default='Malay', choices=LANGUAGE)
	remark         = models.TextField(max_length=254, null=True, blank=True)
	description    = models.TextField( max_length=254, null=True, blank=True)
	game_count     = models.IntegerField(default=0)
	user_link      = models.CharField( max_length=50, null=True, blank=True)

	bank_name      = models.ForeignKey(Bank, on_delete=models.CASCADE, null=True, blank=True)
	account_name   = models.CharField( max_length=254, null=True, blank=True)
	account_number = models.CharField( max_length=254, null=True, blank=True)
	bank_message   = models.TextField(max_length=3000, null=True, blank=True)
	Bank_remark    = models.TextField( max_length=3000, null=True, blank=True)
	Bank_status    = models.CharField(max_length=80, default='Active', choices=STATUS)

	#date & time
	date_created = models.DateTimeField(auto_now_add=True)
	date_updated = models.DateTimeField(auto_now=True)

	def __str__(self):
		return "PHX%06d" % (self.id)


class CustomerGame(models.Model):

	STATUS =	(
		('Active','Active'),
		('Inactive','Inactive'),
	)
	
	customerID = models.ForeignKey(Customer, on_delete=models.CASCADE)
	game_name  = models.ForeignKey(Game, on_delete=models.CASCADE)
	username   = models.CharField(max_length=200, null=True,blank=True)
	password   = models.CharField(max_length=200, null=True,blank=True)
	message    = models.TextField("Message" , max_length=254, null=True, blank=True)
	remark     = models.TextField("Remark" , max_length=254, null=True, blank=True)
	status     = models.CharField(max_length=80, default='Active', choices=STATUS)
	
	#date & time
	date_created = models.DateTimeField(auto_now_add=True)
	date_updated = models.DateTimeField(auto_now=True)

	def __str__(self):
		return self.username


class CustomerBank(models.Model):

	STATUS =	(
		('Active','Active'),
		('Inactive','Inactive'),
	)
	
	customer       = models.ForeignKey(Customer, on_delete=models.CASCADE)
	bank_name      = models.ForeignKey(Bank, on_delete=models.CASCADE)
	account_name   = models.CharField(max_length=200, null=True,blank=True)
	account_number = models.CharField(max_length=200, null=True,blank=True)
	message        = models.TextField("Message" , max_length=3000, null=True, blank=True)
	remark         = models.TextField("Remark" , max_length=3000, null=True, blank=True)
	status         = models.CharField(max_length=80, default='Active', choices=STATUS)
	
	#date & time
	date_created = models.DateTimeField(auto_now_add=True)
	date_updated = models.DateTimeField(auto_now=True)

	def __str__(self):
		return "BANK%06d" % self.id



class Transaction(models.Model):
	STATUS = (
		('Pending','Pending'),
		('Approved','Approved'),
		('Rejected','Rejected'),
	)

	TAG = (
		('Deposit','Deposit'),
		('Free','Free'),
		('Recommend','Recommend'),
		('Lock','Lock'),
		('Borrow','Borrow'),
		('Withdrawal','Withdrawal'),
		('Transfer','Transfer'),
		('Add_Credit','Add Credit'),
		('Deduct_Credit','Deduct Credit'),
	)

	COMPLETE = (
		('Yes','Yes'),
		('No','No'),
	)

	# deposit_id    = id
	admin                = models.CharField(max_length=200, blank=False,null=False)
	customer             = models.ForeignKey(Customer, null=True, on_delete= models.SET_NULL)
	game_backend         = models.ForeignKey(Game, null=True, on_delete= models.SET_NULL , related_name='game_backend')
	game                 = models.ForeignKey(CustomerGame, null=True, on_delete= models.SET_NULL , related_name='game')
	game2                = models.ForeignKey(CustomerGame,blank=True, null=True, on_delete= models.SET_NULL , related_name='game2')
	bank                 = models.ForeignKey(Bank, null=True,blank=True, on_delete= models.SET_NULL)
	customer_bank        = models.ForeignKey(CustomerBank, null=True,blank=True, on_delete= models.SET_NULL)
	promotion            = models.ForeignKey(Promotion, null=True,blank=True, on_delete= models.SET_NULL)
	max_withdrawal       = models.IntegerField(default=0)
	last_topup       	 = models.FloatField(default=0)
	status               = models.CharField(max_length=200, default='Pending', choices=STATUS)
	completed            = models.CharField(max_length=200, default="No", choices=COMPLETE)
	tag                  = models.CharField(max_length=200, default="None", choices=TAG)
	remark               = models.TextField(max_length=254, null=True, blank=True)
	message              = models.TextField(max_length=254, null=True, blank=True)
	date                 = models.DateField(null=True, blank=True)
	time                 = models.TimeField(null=True, blank=True)
	amount               = models.FloatField(default=0.00, blank=False)
	amount_free          = models.FloatField(default=0.00, blank=False)
	amount_promo         = models.FloatField(default=0.00, blank=False)
	amount_tip           = models.FloatField(default=0.00, blank=False)
	amount_void          = models.FloatField(default=0.00, blank=False)
	payback              = models.FloatField(default=0.00 , blank=True, null=True)
	withdrawal_limit_min = models.FloatField(default=0.00)
	withdrawal_limit_max = models.FloatField(default=0.00, null=True, blank=True)
	action_approve       = models.DateTimeField(null=True, blank=True)
	action_reject        = models.DateTimeField(null=True, blank=True)
	action_complete      = models.DateTimeField(null=True, blank=True)
	#date & time
	date_created       = models.DateTimeField(auto_now_add=True)
	date_updated       = models.DateTimeField(auto_now=True)
	# recommend
	recommend_username = models.CharField( max_length=254 , blank=True)
	recommend_phone    = models.CharField( max_length=254 , blank=True)

	def __str__(self):
		if self.tag == "Deposit":
			if self.bank:
				bbcode = self.bank.bank_code
			else:
				bbcode = ""
			return "D%06d" % self.id + bbcode
		if self.tag == "Free":
			return "F%06d" % self.id
		if self.tag == "Borrow":
			return "B%06d" % self.id
		if self.tag == "None":
			return "N%06d" % self.id
		if self.tag == "Recommend":
			return "R%06d" % self.id
		if self.tag == "Lock":
			return "L%06d" % self.id
		if self.tag == "Withdrawal":
			if self.bank:
				return "W%06d" % self.id + self.bank.bank_code
			else:
				return "W%06d" % self.id
		if self.tag == "Transfer":
			return "T%06d" % self.id
		if self.tag == "Add_Credit":
			return "CC%06d" % self.id
		if self.tag == "Deduct_Credit":
			return "CD%06d" % self.id






# class CustomerBankAccount(models.Model):
# 	customer       = models.ForeignKey(Customer, on_delete=models.CASCADE, null=True)
# 	bank           = models.ForeignKey(Bank, on_delete=models.SET_NULL, null=True)
# 	account_name   = models.CharField( max_length=254, null=True, blank=True)
# 	account_number = models.CharField( max_length=254, null=True, blank=True)

# 	def __str__(self):
# 	 return self.account_name

























# class Tag(models.Model):
# 	name = models.CharField(max_length=200, null=True)
# 	date_created = models.DateTimeField(auto_now_add=True)
# 	date_updated = models.DateTimeField(auto_now=True)
	
# 	def __str__(self):
# 	 return self.name

# #product = games
# class Product(models.Model):
# 	CATEGORY =	(
# 		('Indoor','Indoor'),
# 		('Outdoor','Outdoor'),
# 	)

# 	name 		= models.CharField(max_length=200, null=True)
# 	price 		= models.FloatField(null=True)
# 	category 	= models.CharField(max_length=200, null=True, choices=CATEGORY)
# 	description = models.CharField(max_length=200, null=True, blank=True)
# 	tags		= models.ManyToManyField(Tag)
# 	date_create = models.DateTimeField(auto_now_add=True, null=True)
# 	date_created = models.DateTimeField(auto_now_add=True)
# 	date_updated = models.DateTimeField(auto_now=True)

# 	def __str__(self):
# 	 return self.name



# class Order(models.Model):
# 	STATUS = (
# 		('Pending','Pending'),
# 		('rejected','rejected'),
# 		('approved','approved'),
# 	)

# 	customer	= models.ForeignKey(Customer, null=True, on_delete= models.SET_NULL)
# 	product		= models.ForeignKey(Product, null=True, on_delete= models.SET_NULL)
# 	date_created= models.DateTimeField(auto_now_add=True, null=True)
# 	status 		= models.CharField(max_length=200, null=True, choices=STATUS)
# 	note 		= models.CharField(max_length=1000, null=True)
# 	date_created = models.DateTimeField(auto_now_add=True)
# 	date_updated = models.DateTimeField(auto_now=True)
	

# 	def __str__(self):
# 	 return self.product.name


class SMSGateway(models.Model):
	token = models.CharField(max_length=254, null=False, blank=False)
	deviceId = models.CharField(max_length=254, null=False, blank=False, unique=True)
	active = models.IntegerField(default=0)

	def __str__(self):
	 return self.deviceId


class Positions(models.Model):
	group = models.CharField(max_length=254, null=False, blank=False)
	name = models.CharField(max_length=254, null=False, blank=False)
	codename = models.CharField(max_length=254, null=False, blank=False, unique=True)

	def __str__(self):
	 return self.codename


class User_Position(models.Model):
	user  = models.ForeignKey(User, on_delete=models.CASCADE)
	position = models.ForeignKey(Positions, on_delete=models.CASCADE)

	def __str__(self):
	 return "USERPOS%06d" % self.id


class ActionLogs(models.Model):
	action = models.CharField(max_length=254, null=False, blank=False)
	description = models.CharField(max_length=254, null=False, blank=False)
	remark = models.CharField(max_length=254, null=False, blank=False)
	date_created = models.DateTimeField(auto_now_add=True)
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	remote_ip = models.CharField(max_length=254, null=False, blank=False)
	device = models.CharField(max_length=254, null=False, blank=False)

	def __str__(self):
		return "ACTION%06d" % self.id