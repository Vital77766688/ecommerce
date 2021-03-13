from decimal import Decimal

from store.models import Product


class Cart:
	def __init__(self, request):
		self.session = request.session
		cart = self.session.get('skey')
		if not cart:
			cart = self.session['skey'] = {}
		self.cart = cart

	def __len__(self):
		return sum([item['qty'] for item in self.cart.values()])

	def __iter__(self):
		ids = self.cart.keys()
		products = Product.objects.filter(id__in=ids)
		
		cart = self.cart.copy()

		for product in products:
			cart[str(product.id)]['product'] = product

		for item in cart.values():
			yield item

	def add(self, product, qty):
		id = str(product.id)
		if id in self.cart:
			self.cart[id]['qty'] = qty
		else:
			self.cart[id] = {'price': str(product.price), 'qty': qty}
		self.save()

	def delete(self, id):
		del self.cart[str(id)]
		self.save()

	def clean(self):
		del self.session['skey']

	@property
	def total_price(self):
		return sum(Decimal(item['price']) * item['qty'] for item in self.cart.values())

	def save(self):
		self.session.modified = True