from .models import *

def get_client_ip(request):
	x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
	if x_forwarded_for:
		ip = x_forwarded_for.split(',')[0]
	else:
		ip = request.META.get('REMOTE_ADDR')
	return ip

def add_action_log(request, action, description, remark = ''):
	log = ActionLogs()
	log.action = action
	log.description = description
	log.remark = remark
	log.user_id = request.user.id
	log.remote_ip = get_client_ip(request)
	log.device = 'desktop'
	log.save()

def add_action_log_click(request, where):
	action = 'Clicked'
	description = request.user.username + ' clicked ' + where
	add_action_log(request, action, description)

def add_action_log_create(request, value):
	action = "Create"
	description = "%s create %s" % (request.user.username, value)
	add_action_log(request, action, description)

def add_action_log_update(request, value):
	action = "Update"
	description = "%s update %s" % (request.user.username, value)
	add_action_log(request, action, description)

def add_action_log_delete(request, value):
	action = "Delete"
	description = "%s delete %s" % (request.user.username, value)
	add_action_log(request, action, description)

def add_action_log_transaction(request, message):
	action = "Transaction"
	description = "%s by %s" % (message, request.user.username)
	add_action_log(request, action, description)