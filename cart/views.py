import json

from django.http import JsonResponse, HttpResponse
from django.shortcuts import get_object_or_404, render

from store.models import Product

from .cart import Cart


def cart_summary(request):
	return render(request, 'cart/cart_summary.html')
