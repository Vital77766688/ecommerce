import json

from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render

from store.models import Product

from .cart import Cart


def cart_summary(request):
	return render(request, 'cart/cart_summary.html')


def update_cart(request):
	cart = Cart(request)
	
	if request.method == 'POST':
		data = json.loads(request.body.decode())
		product_id = data.get('productId')
		qty = data.get('qty')
		if not product_id or not qty:
			return JsonResponse({'success': False, 'message': 'Bad request'}, status=400)
		product = get_object_or_404(Product, id=product_id)
		cart.add(product, qty)
		return JsonResponse({'success': True, 'message': 'Product added', 'data': {'qty': len(cart)}}, status=201)
	
	elif request.method == 'DELETE':
		id = json.loads(request.body.decode()).get('id')
		if not id:
			return JsonResponse({'success': False, 'message': 'Bad request'}, status=400)
		cart.delete(id)
		return JsonResponse({'success': True, 'message': 'Product deleted', 
							 'data': {'qty': len(cart), 'total_price': cart.total_price}},
							status=200)

	elif request.method == 'PATCH':
		data = json.loads(request.body.decode())
		id = data.get('id')
		qty = data.get('qty')
		if not id or not qty:
			return JsonResponse({'success': False, 'message': 'Bad request'}, status=400)
		cart.update(id, qty)
		return JsonResponse({'success': True, 'message': 'Product updated', 
							 'data': {'qty': len(cart), 'total_price': cart.total_price}},
							status=200)		
	else:
		return JsonResponse({'success': False, 'message': 'Method not allowed'}, status=405)