from decimal import Decimal

from django.utils.translation import gettext_lazy as _

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

	def update(self, id, price, qty):
		if self.isin(id):
			self.update_product(id, qty)
			return _('Product updated')
		self.add_product(id, price, qty)
		return _('Product added')

	def add_product(self, id, price, qty):
		self.cart[id] = {'price': str(price), 'qty': qty}
		self.save()

	def update_product(self, id, qty):
		self.cart[id]['qty'] = qty
		self.save()

	def delete(self, id):
		del self.cart[str(id)]
		self.save()

	def clean(self):
		del self.session['skey']

	@property
	def total_price(self):
		return sum(Decimal(item['price']) * item['qty'] for item in self.cart.values())

	def isin(self, id):
		return id in self.cart

	def save(self):
		self.session.modified = True