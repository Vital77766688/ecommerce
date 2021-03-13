from django.test import TestCase

from tags_and_filters.templatetags.math import multiply


class TestMath(TestCase):
	def test_multiply(self):
		self.assertEqual(multiply(2,3), 6)