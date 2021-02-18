from django.utils.translation import gettext_lazy as _
from django.contrib.auth.base_user import BaseUserManager, AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.db import models


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
	is_email_verified = models.BooleanField(_('Email Verified'), default=False)
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