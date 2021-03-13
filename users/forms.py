from django import forms

from .models import UserProfile, UserAddress


class UserProfileForm(forms.ModelForm):
	class Meta:
		model = UserProfile
		fields = ['first_name', 'last_name', 'phone_number', 'image']


class UserAddressForm(forms.ModelForm):
	class Meta:
		model = UserAddress
		fields = [
			'country', 'region', 'city', 'street', 
			'building_number', 'block', 'entrance',
			'appartment', 'is_private_house', 'zip_code'
		]
