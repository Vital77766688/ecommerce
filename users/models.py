from django.utils.translation import gettext_lazy as _
from django.contrib.auth.base_user import BaseUserManager, AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.db import models

from phonenumber_field.modelfields import PhoneNumberField
from django_countries.fields import CountryField


class UserManager(BaseUserManager):
	"""
	Custom user manager where email is used as unique identifier for authentication
	"""
	def create_user(self, email, password, **kwargs):
		if not email:
			raise ValueError('You should provide the email')
		
		email = self.normalize_email(email)
		
		user = self.model(email=email, **kwargs)
		user.set_password(password)
		user.save()

		return user

	def create_superuser(self, email, password, **kwargs):
		kwargs.setdefault('is_staff', True)
		kwargs.setdefault('is_superuser', True)

		return self.create_user(email, password, **kwargs)


class User(AbstractBaseUser, PermissionsMixin):
	email = models.EmailField(_('Email Address'), max_length=150, unique=True)
	is_staff = models.BooleanField(_('Staff'), default=False)
	is_active = models.BooleanField(_('Active'), default=True)
	date_joined = models.DateTimeField(_('Date joined'), auto_now_add=True)

	USERNAME_FIELD = 'email'
	REQUIRED_FIELDS = []

	objects = UserManager()

	def __str__(self):
		return self.email

	class Meta:
		db_table = 'users'


class UserProfile(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
	first_name = models.CharField(_('First Name'), max_length=80)
	last_name = models.CharField(_('Last Name'), max_length=80)
	phone_number = PhoneNumberField(_('Phone Number'))
	image = models.ImageField(_('User Image'), upload_to='images/users/', default='images/user_default.jpeg')

	def __str__(self):
		return f"{self.first_name} {self.last_name}"

	class Meta:
		verbose_name = _('User Profile')
		verbose_name_plural = _('User Profiles')
		db_table = 'user_profile'


class UserAddress(models.Model):
	user = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='addresses')
	country = CountryField(_('Country'))
	region = models.CharField(_('Region'), max_length=50)
	city = models.CharField(_('City'), max_length=50)
	street = models.CharField(_('Street'), max_length=50)
	building_number = models.CharField(_('# of building'), max_length=10)
	block = models.CharField(_('Block'), max_length=10, null=True, blank=True)
	entrance = models.CharField(_('# of entrance'), max_length=10, null=True, blank=True)
	appartment = models.CharField(_('# of appartment'), max_length=10, null=True, blank=True)
	is_private_house = models.BooleanField(_('Private house'), default=False)
	zip_code = models.CharField(_('ZIP Code'), max_length=10)
	create_date = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		fields = [
			self.country.name, 
			self.region,
			self.city,
			f"{self.street} str.",
			self.building_number
		]

		if self.block:
			fields.append(f"block: {self.block}")

		if self.entrance:
			fields.append(f"entrance: {self.entrance}")

		if self.appartment:
			fields.append(f"appartment: {self.appartment}")

		return ', '.join(fields)

	class Meta:
		verbose_name = _('User Address')
		verbose_name_plural = _('User Addresses')
		db_table = 'user_address'
