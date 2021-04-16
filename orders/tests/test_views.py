from importlib import import_module

from django.conf import settings
from django.http import HttpRequest
from django.test import Client, TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model

from users.models import UserAddress
from cart.cart import Cart
from store.models import Product, Category
from orders.models import Order, OrderStatus

User = get_user_model()


class TestCheckout(TestCase):
	def setUp(self):
		self.client = Client()
		self.user = User.objects.create_user(email='a@a.com', password='test123456')
		self.client.login(email='a@a.com', password='test123456')

		OrderStatus.objects.create(status_name='placed')

		self.address1 = UserAddress.objects.create(
			user=self.user.profile,
			country='KZ',
			region='A',
			city='A',
			street='a',
			building_number='11',
			block='1',
			is_private_house=False,
			entrance='1',
			appartment='1',
			zip_code='000'
		)

		self.address2 = UserAddress.objects.create(
			user=self.user.profile,
			country='KZ',
			region='A',
			city='A',
			street='a',
			building_number='11',
			block='1',
			is_private_house=False,
			entrance='1',
			appartment='1',
			zip_code='000'
		)

		category = Category.objects.create(category_name='aaa', category_slug='aaa')
		product = Product.objects.create(category=category, product_name='qqq', product_slug='qqq', price=10.00)
		self.client.post(
					reverse('cart_api:update_cart'),
					{
						'id': 1,
						'qty': 3
					},
					content_type='application/json'
				)


	def test_checkout_page(self):
		response = self.client.get(reverse('orders:checkout'))

		self.assertEqual(response.status_code, 200)

		html = response.content.decode('utf8')
		self.assertIn('<title>MyStore: Checkout</title>', html)

	def test_checkout_new_address(self):
		response = self.client.post(
			reverse('orders:checkout'),
			{
				'country': 'KZ',
				'region': 'A',
				'city': 'A',
				'street':'a',
				'building_number': '11',
				'block': '1',
				'is_private_house': False,
				'entrance': '1',
				'appartment': '1',
				'zip_code': '000',
				'new_address': ''
			}
		)
		self.assertEqual(self.user.profile.addresses.count(), 3)
		self.assertEqual(response.status_code, 302)

	def test_place_order(self):
		response = self.client.post(
			reverse('orders:checkout'),
			{
				'delivery_address': self.address1.id,
				'billing_address': self.address2.id,
				'comment': '',
				'is_billing_same': False
			}
		)

		self.assertEqual(response.status_code, 302)
		self.assertEqual(Order.objects.get(pk=1).items.count(), 1)

	def test_place_order_same_billing_address(self):
		response = self.client.post(
			reverse('orders:checkout'),
			{
				'delivery_address': self.address1.id,
				'billing_address': self.address2.id,
				'comment': '',
				'is_billing_same': True
			}
		)

		order = Order.objects.get(pk=1)
		self.assertEqual(order.delivery_address, order.billing_address)		


class TestOrders(TestCase):
	def test_orders_page(self):
		user = User.objects.create_user(email='a@a.com', password='test123456')
		client = Client()
		client.login(email='a@a.com', password='test123456')
		response = client.get(reverse('orders:orders'))

		self.assertEqual(response.status_code, 200)

		html = response.content.decode('utf8')
		self.assertIn('<title>MyStore: My orders</title>', html)