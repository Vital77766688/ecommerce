from django.test import TestCase

from users.models import User, UserProfile, UserAddress


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


class TestUserProfile(TestCase):
	def setUp(self):
		self.user = User.objects.create_user(email='a@a.com', password='test123456')

	def test_create_profile(self):
		profile = UserProfile.objects.filter(user=self.user)
		self.assertTrue(profile.exists())
		profile = profile[0]
		profile.first_name = 'A'
		profile.last_name = 'B'
		profile.save()
		self.assertTrue(isinstance(profile, UserProfile))
		self.assertEqual(str(profile), 'A B')


class TestUserAddress(TestCase):
	def setUp(self):
		self.user = User.objects.create_user(email='a@a.com', password='test123456')
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
			country='RU',
			region='M',
			city='M',
			street='m',
			building_number='1',
			is_private_house=True,
			zip_code='000'
		)

	def test_user_address_string(self):
		self.assertEqual(str(self.address1), 'Kazakhstan, A, A, a str., 11, block: 1, entrance: 1, appartment: 1')
		self.assertEqual(str(self.address2), 'Russia, M, M, m str., 1')