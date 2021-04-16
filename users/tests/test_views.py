import json

from django.test import Client, TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model

from orders.models import Order, OrderStatus
from users.models import UserProfile, UserAddress

User = get_user_model()


class TestProfileView(TestCase):
	def setUp(self):
		self.client = Client()
		self.user = User.objects.create_user(email='a@a.com', password='test123456')
		self.address1 = UserAddress.objects.create(
			user=self.user.profile,
			country='RU',
			region='M',
			city='M',
			street='m',
			building_number='1',
			is_private_house=True,
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
		OrderStatus.objects.create(status_name='placed')
		Order.objects.create(
			user=self.user.profile,
			delivery_address=self.address1,
			billing_address=self.address1,
			price=10.00
		)
		self.client.login(email='a@a.com', password='test123456')

	def test_profile_page_not_logged_in(self):
		self.client.logout()
		response = self.client.get(reverse('users:profile'))
		self.assertEqual(response.status_code, 302)
		self.assertIn(reverse('account_login'), response._headers['location'][1])

	def test_profile_page_logged_in(self):
		response = self.client.get(reverse('users:profile'))
		self.assertEqual(response.status_code, 200)
		html = response.content.decode('utf8')
		self.assertIn('<title>MyStore: Profile</title>', html)

	def test_profile_update(self):
		response = self.client.post(
			reverse('users:profile'),
			{
				'first_name': 'a',
				'last_name': 'b',
				'phone_number': '+77071234567',
				'image': '',
				'profile': ''
			}
		)
		self.assertEqual(response.status_code, 302)
		
		profile = UserProfile.objects.get(user=self.user)
		self.assertEqual(profile.first_name, 'a')
		self.assertEqual(profile.last_name, 'b')
		self.assertEqual(profile.phone_number, '+77071234567')

	def test_password_change(self):
		response = self.client.post(
			reverse('users:profile'),
			{
				'oldpassword': 'test123456',
				'password1': 'test654321',
				'password2': 'test654321',
				'change_password': ''
			}
		)

		self.assertEqual(response.status_code, 302)
		self.assertIn('_auth_user_id', self.client.session)

	def test_add_new_address(self):
		response = self.client.post(
			reverse('users:profile'),
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

		self.assertEqual(response.status_code, 302)
		profile = UserProfile.objects.get(user=self.user)
		self.assertEqual(profile.addresses.count(), 3)

	def test_delete_address_fail(self):
		response = self.client.post(
			reverse('users:profile'),
			{
				'id': self.address1.id,
				'delete_address': ''
			}
		)

		self.assertEqual(response.status_code, 302)
		profile = UserProfile.objects.get(user=self.user)
		self.assertEqual(profile.addresses.count(), 2)

	def test_delete_address_success(self):
		response = self.client.post(
			reverse('users:profile'),
			{
				'id': self.address2.id,
				'delete_address': ''
			}
		)

		self.assertEqual(response.status_code, 302)
		profile = UserProfile.objects.get(user=self.user)
		self.assertEqual(profile.addresses.count(), 1)

	def test_change_address(self):
		response = self.client.post(
			reverse('users:profile'),
			{
				'user': self.user.profile,
				'country': 'RU',
				'region': 'M',
				'city': 'S',
				'street': 'm',
				'building_number': '1',
				'is_private_house': True,
				'zip_code': '000',
				'change_address': 2
			}
		)

		self.assertEqual(response.status_code, 302)
		address = UserAddress.objects.get(id=self.address2.id)
		self.assertEqual(str(address), 'Russia, M, S, m str., 1')


class TestGetAddress(TestCase):
	def setUp(self):
		self.client = Client()
		self.user = User.objects.create_user(email='a@a.com', password='test123456')
		self.address1 = UserAddress.objects.create(
			user=self.user.profile,
			country='RU',
			region='M',
			city='M',
			street='m',
			building_number='1',
			is_private_house=True,
			zip_code='000'
		)
		self.client.login(email='a@a.com', password='test123456')

	def test_get_address_api_success(self):
		response = self.client.get(
			f"{reverse('users_api:address')}?id={self.address1.id}",
		)

		self.assertEqual(response.status_code, 200)
		data = json.loads(response.content.decode('utf8'))
		self.assertEqual(data['street'], 'm')

	def test_get_address_api_fail(self):
		response = self.client.post(
			reverse('users_api:address'),
			{
				'id': self.address1.id
			}
		)

		self.assertEqual(response.status_code, 405)

		response = self.client.get(
			reverse('users_api:address'),
		)

		self.assertEqual(response.status_code, 404)