from django.test import TestCase

from store.models import Category, Product


class TestCategories(TestCase):
	def setUp(self):
		self.data = Category.objects.create(category_name='Books', category_slug='books')

	def test_category_entry(self):
		self.assertTrue(isinstance(self.data, Category))
		self.assertEqual(str(self.data), 'Books')


class TestProducts(TestCase):
	def setUp(self):
		self.category = Category.objects.create(category_name='Books', category_slug='books')
		self.product = Product.objects.create(category=self.category, 
											  product_name='Harry Potter', 
											  product_slug='harry-potter',
											  price=12.99)

	def test_product_entry(self):
		self.assertTrue(isinstance(self.product, Product))
		self.assertEqual(str(self.product), 'Harry Potter')
		self.assertEqual(str(self.product.category), 'Books')