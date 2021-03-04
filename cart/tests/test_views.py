from django.test import Client, TestCase
from django.urls import reverse

from store.models import Category, Product


class TestCartView(TestCase):
	def setUp(self):
		self.url = reverse('cart:update_cart')
		self.client = Client()
		self.books = Category.objects.create(category_name='Books', category_slug='books')
		self.cds = Category.objects.create(category_name='CDs', category_slug='cds')
		self.product1 = Product.objects.create(category=self.books,
											  product_name='Harry Potter',
											  product_slug='harry-potter',
											  price=19.99)
		self.product2 = Product.objects.create(category=self.cds,
											  product_name='Arch Enemy - War Eternal',
											  product_slug='arch-enemy-war-eternal',
											  price=15.99)
		self.product3 = Product.objects.create(category=self.cds,
											  product_name='Sabaton - The Great War',
											  product_slug='sabaton-great-war',
											  price=15.99)

		self.client.post(self.url, {
					'id': self.product3.id,
					'qty': 1
				}, content_type='application/json')


	def test_cart_url(self):
		response = self.client.get(reverse('cart:cart_summary'))
		self.assertEqual(response.status_code, 200)
		
		html = response.content.decode('utf8')
		self.assertIn('<title>MyStore: Cart Summary</title>', html)

	def test_add_to_cart(self):
		response = self.client.post(self.url, {
			'id': self.product1.id,
			'qty': 1
		}, content_type='application/json')
		self.assertEqual(response.status_code, 201)
		self.assertEqual(response.json(), {'success': True, 'message': 'Product added', 'data': {'cart_qty': 2}})

		response = self.client.post(self.url, {
			'id': self.product2.id,
			'qty': 4
		}, content_type='application/json') 
		self.assertEqual(response.status_code, 201)
		self.assertEqual(response.json(), {'success': True, 'message': 'Product added', 'data': {'cart_qty': 6}})

		response = self.client.post(self.url, {
			'id': self.product3.id,
			'qty': 2
		}, content_type='application/json')
		self.assertEqual(response.status_code, 201)
		self.assertEqual(response.json(), {'success': True, 'message': 'Product added', 'data': {'cart_qty': 7}})

		response = self.client.post(self.url, 
							   		{'id': self.product1.id}, 
							   		content_type='application/json')
		self.assertEqual(response.status_code, 400)

	def test_update_cart(self):
		response = self.client.post(self.url, {
			'id': self.product3.id,
			'qty': 4
		}, content_type='application/json')
		self.assertEqual(response.status_code, 201)
		self.assertEqual(response.json(), {'success': True, 
										   'message': 'Product added', 
										   'data': {'cart_qty': 4}})
		response = self.client.post(self.url, {
			'id': self.product3.id
		}, content_type='application/json')
		self.assertEqual(response.status_code, 400)

	def test_delete_from_cart(self):
		response = self.client.delete(self.url, {'id': self.product3.id}, content_type='application/json')
		self.assertEqual(response.status_code, 204)
		response = self.client.delete(self.url, {}, content_type='application/json')
		self.assertEqual(response.status_code, 400)

	def test_not_allowed_method(self):
		response = self.client.get(self.url)
		self.assertEqual(response.status_code, 405)

	def test_qty_wrong_type(self):
		response = self.client.post(self.url, {
			'id': self.product3.id,
			'qty': '2ee'
		}, content_type='application/json')
		self.assertEqual(response.status_code, 400)