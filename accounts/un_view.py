#hold un-use functions


@unauthenticated_user
def registerPage(request):

	form = CreateUserForm()
	if request.method == 'POST':
		form = CreateUserForm(request.POST)
		if form.is_valid():
			user = form.save()
			username = form.cleaned_data.get('username')
			messages.success(request, 'Account was created for ' + username)
			return redirect('login')
		

	context = {'form':form}
	return render(request, 'accounts/register.html', context)




# @login_required(login_url='login')
# @allowed_users(allowed_roles=['admin'])
def updateOrder(request,pk):
	
	order = Order.objects.get(id=pk)
	form = OrderFrom(instance=order)

	if request.method == "POST":
		# print('Printing Post:', request.POST)
		form = OrderFrom(request.POST, instance=order )
		if form.is_valid():
			form.save()
			return redirect('/')
	context = {'form':form}
	return render(request, 'accounts/order_form.html',  context)


# @login_required(login_url='login')
# @allowed_users(allowed_roles=['admin'])
def deleteOrder(request,pk):
	order = Order.objects.get(id=pk)
	if request.method == "POST":
		order.delete()
		return redirect('/')

	context = {'item':order}
	return render(request, 'accounts/delete.html',  context)




# customer profile go in
# @login_required(login_url='login')
# @allowed_users(allowed_roles=['customer'])
def userPage(request):
	orders 	= request.user.customer.order_set.all()
	total_orders= orders.count()
	approved 	= orders.filter(status='approved').count()
	pending 	= orders.filter(status='Pending').count()
	context = {'orders' : orders,'total_orders': total_orders,'approved': approved, 'pending' : pending}
	return render(request, 'accounts/user.html', context)






# @login_required(login_url='login')
# @allowed_users(allowed_roles=['admin'])
def createOrder(request,pk):
	OrderFromSet = inlineformset_factory(Customer, Order , fields=('product' , 'status'), extra=5)
	customer = Customer.objects.get(id=pk)
	formSet = OrderFromSet(queryset=Order.objects.none(), instance=customer)

	# form = OrderFrom(initial={'customer': customer})
	if request.method == "POST":
		# print('Printing Post:', request.POST)
		formSet = OrderFromSet(request.POST, instance=customer)
		# form = OrderFrom(request.POST)
		if formSet.is_valid():
			formSet.save()
			return redirect('/')

	context = {'formSet':formSet, 'customer':customer}
	return render(request, 'accounts/order_form.html',  context)






# @login_required(login_url='login')
# @allowed_users(allowed_roles=['customer', 'admin'])
def accountSettings(request):
	customer 	= request.user.customer
	form 	= CustomerForm(instance=customer)

	if request.method == "POST":
		form = CustomerForm(request.POST, request.FILES, instance=customer)
		if form.is_valid:
			form.save()

	context =	{'form':form}
	return render(request, 'accounts/account_settings.html', context)

# @login_required(login_url='login')
# @allowed_users(allowed_roles=['admin'])
def products(request):
	products = Product.objects.all()
	return render(request, 'accounts/products.html', {'products' : products})






























