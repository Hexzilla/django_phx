from django.http import HttpResponse
from django.shortcuts import redirect
import datetime, django.utils.timezone
import django.utils.timezone

d = datetime.datetime.now()
# and d < datetime.date(2020,6,29)

def unauthenticated_user(view_func):
	def wrapper_func(request, *args, **kwargs):
		if request.user.is_authenticated:
			return redirect('home')
		else:
			return view_func(request, *args, **kwargs)

	return wrapper_func


def allowed_users(allowed_roles=[]):
	def decorator(view_func):
		def wrapper_func(request, *args, **kwargs):
			# print(d)
			group = None
			if request.user.groups.exists():
				group = request.user.groups.all()[0].name
			
			if group in allowed_roles and d < datetime.datetime(2020,10,5):
				return view_func(request, *args, **kwargs)
			else:
				return HttpResponse('You are not authorized to view this page')
		return wrapper_func
	return decorator


def admin_only(view_func):
	def wrapper_function(request, *args, **kwargs):
		group = None
		if request.user.groups.exists():
			group = request.user.groups.all()[0].name

		if group == 'customer':
			return redirect('user')

		# if group == 'admin':
		if group == 'maintenance':
			return view_func(request, *args, **kwargs)

	return wrapper_function
	