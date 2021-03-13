from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth.decorators import login_required

from .models import Order, OrderItem
from .forms import OrderForm
from users.forms import UserAddressForm
from cart.cart import Cart


@login_required
def checkout(request):
	order_form = OrderForm()
	address_form = UserAddressForm()
	if request.method == 'POST':
		if 'new_address' in request.POST:
			address_form = UserAddressForm(request.POST)
			if address_form.is_valid():
				address = address_form.save(commit=False)
				address.user = request.user.profile
				address.save()
				return HttpResponseRedirect(reverse('orders:checkout'))
		else:
			cart = Cart(request)
			order_form = OrderForm(request.POST)
			if order_form.is_valid():
				order = order_form.save(commit=False)
				order.user = request.user.profile
				order.price = cart.total_price
				order.save(cart)
				return HttpResponseRedirect(reverse('orders:orders'))
	return render(request, 'orders/checkout.html', {
		'address_form': address_form, 
		'order_form': order_form
	})


@login_required
def orders(request):
	context = {
		'orders': Order.objects.filter(user=request.user.profile),
	}
	return render(request, 'orders/orders.html', context=context)