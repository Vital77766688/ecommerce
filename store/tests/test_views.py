from django.test import Client, TestCase
from django.urls import reverse

from store.models import Category, Product


class TestViews(TestCase):
	def setUp(self):
		self.client = Client()
		self.category = Category.objects.create(category_name='Books', category_slug='books')
		self.product = Product.objects.create(category=self.category,
											  product_name='Harry Potter',
											  product_slug='harry-potter',
											  price=19.99)

	def test_homepage(self):
		response = self.client.get('/')
		self.assertEqual(response.status_code, 200)
		
		html = response.content.decode('utf8')
		self.assertIn('<title>MyStore</title>', html)

	def test_product_list(self):
		response = self.client.get(
			reverse('store:category_list', args=['books'])
		)
		self.assertEqual(response.status_code, 200)

		html = response.content.decode('utf8')
		self.assertIn('<title>MyStore: Books</title>', html)

	def test_product_details(self):
		response = self.client.get(
			reverse('store:product_details', args=['harry-potter'])
		)
		self.assertEqual(response.status_code, 200)

		html = response.content.decode('utf8')
		self.assertIn('<title>MyStore: Harry Potter</title>', html)
