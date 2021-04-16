from decimal import Decimal

from django.test import TestCase

from users.models import User, UserProfile, UserAddress
from store.models import Product, Category
from orders.models import OrderStatus, Order, OrderItem


class TestOrderStatus(TestCase):
	def test_order_status_string(self):
		status = OrderStatus.objects.create(status_name='placed')
		self.assertEqual(str(status), 'placed')


class TestOrder(TestCase):
	def setUp(self):
		self.user = User.objects.create_user(email='a@a.com', password='test123456')
		self.profile = self.user.profile
		self.address = UserAddress.objects.create(
			user=self.user.profile,
			country='RU',
			region='M',
			city='M',
			street='m',
			building_number='1',
			is_private_house=True,
			zip_code='000'
		)
		self.status = OrderStatus.objects.create(status_name='placed')
		self.order = Order.objects.create(
			user=self.profile,
			delivery_address=self.address,
			billing_address=self.address,
			status=self.status,
			price=10.00,
			comment='ZBS'
		)

	def test_order_string(self):
		self.assertEqual(str(self.order), 'a@a.com: 1')

	def test_order_save(self):
		self.assertEqual(self.order.items_count, 0)


class TestOrderItem(TestCase):
	def setUp(self):
		self.category = Category.objects.create(category_name='aaa', category_slug='aaa')
		self.product = Product.objects.create(
			category=self.category, 
			product_name='qqq', 
			product_slug='qqq', 
			price=10.00
		)
		self.user = User.objects.create_user(email='a@a.com', password='test123456')
		self.address = UserAddress.objects.create(
			user=self.user.profile,
			country='RU',
			region='M',
			city='M',
			street='m',
			building_number='1',
			is_private_house=True,
			zip_code='000'
		)
		self.status = OrderStatus.objects.create(status_name='placed')
		self.order = Order.objects.create(
			user=self.user.profile, 
			delivery_address=self.address, 
			billing_address=self.address, 
			price=10.00
		)
		self.order_item = OrderItem.objects.create(order=self.order, product=self.product, price=10.00, qty=3)

	def test_order_item_string(self):
		self.assertEqual(str(self.order_item), '1: qqq')