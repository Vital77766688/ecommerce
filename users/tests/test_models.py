from django.test import TestCase

from users.models import User


class TestUsers(TestCase):
	def test_create_user(self):
		user = User.objects.create_user(email='a@a.com', password='test123456')
		self.assertTrue(isinstance(user, User))
		self.assertEqual(str(user), 'a@a.com')

		with self.assertRaises(ValueError):
			user = User.objects.create_user(email='', password='test123456')

	def test_create_superuser(self):
		user = User.objects.create_superuser(email='a@a.com', password='test123456')
		self.assertTrue(user.is_superuser)
		self.assertTrue(user.is_staff)