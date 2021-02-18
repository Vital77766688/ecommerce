from django.test import Client, TestCase
from django.urls import reverse

from store.models import Category, Product


class TestViews(TestCase):
	def setUp(self):
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

	def test_homepage(self):
		response = self.client.get('/')
		self.assertEqual(response.status_code, 200)
		
		html = response.content.decode('utf8')
		self.assertIn('<title>MyStore</title>', html)

	def test_products_list(self):
		response = self. client.get(
			reverse('store:category_list', args=['all'])
		)
		self.assertEqual(response.status_code, 200)

		html = response.content.decode('utf8')
		self.assertIn('<title>MyStore: All</title>', html)
		self.assertIn('Harry Potter', html)
		self.assertIn('Arch Enemy - War Eternal', html)

	def test_category_list(self):
		response = self.client.get(
			reverse('store:category_list', args=['books'])
		)
		self.assertEqual(response.status_code, 200)

		html = response.content.decode('utf8')
		self.assertIn('<title>MyStore: Books</title>', html)
		self.assertIn('Harry Potter', html)
		self.assertNotIn('Arch Enemy - War Eternal', html)

	def test_product_details(self):
		response = self.client.get(
			reverse('store:product_details', args=['harry-potter'])
		)
		self.assertEqual(response.status_code, 200)

		html = response.content.decode('utf8')
		self.assertIn('<title>MyStore: Harry Potter</title>', html)
