import json

from django.utils.translation import gettext_lazy as _
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models.deletion import RestrictedError
from django.core.exceptions import ObjectDoesNotExist

from allauth.account.forms import ChangePasswordForm
from allauth.account.utils import logout_on_password_change

from .forms import UserProfileForm, UserAddressForm
from .models import UserAddress


@login_required
def profile(request):
	profile_form = UserProfileForm()
	address_form = UserAddressForm()
	change_password_form = ChangePasswordForm()

	if request.method == 'POST':
		if 'profile' in request.POST:
			profile_form = UserProfileForm(request.POST, 
										   request.FILES, 
										   instance=request.user.profile)
			if profile_form.is_valid():
				profile_form.save()
				messages.add_message(request, messages.SUCCESS, _('Profile has been changed'))
				return HttpResponseRedirect(reverse('users:profile'))

		if 'change_password' in request.POST:
			change_password_form = ChangePasswordForm(request.user, request.POST)
			if change_password_form.is_valid():
				change_password_form.save()
				logout_on_password_change(request, change_password_form.user)
				messages.add_message(request, messages.SUCCESS, _('Your password has been changed'))
				return HttpResponseRedirect(reverse('users:profile'))

		if 'new_address' in request.POST:
			address_form = UserAddressForm(request.POST)
			if address_form.is_valid():
				address = address_form.save(commit=False)
				address.user = request.user.profile
				address.save()
				return HttpResponseRedirect(reverse('users:profile'))

		if 'delete_address' in request.POST:
			address_id = request.POST.get('id')
			if address_id:
				try:
					address = get_object_or_404(UserAddress, id=address_id, user=request.user.profile)
					address.delete()
					messages.add_message(request, messages.SUCCESS, 'Address has been deleted')
				except RestrictedError as e:
					messages.add_message(request, 
										 messages.ERROR, 
										 _('Cannot delete this address, because there are some orders associated with it'))
				return HttpResponseRedirect(reverse('users:profile'))

		if 'change_address' in request.POST:
			address_id = request.POST.get('change_address')
			if address_id:
				address = get_object_or_404(UserAddress, id=address_id, user=request.user.profile)
				address_form = UserAddressForm(request.POST, instance=address)
				if address_form.is_valid():
					address_form.save()
					messages.add_message(request, messages.SUCCESS, _('Address has been changed'))
					return HttpResponseRedirect(reverse('users:profile'))

	context = {
		'profile_form': profile_form,
		'address_form': address_form,
		'change_password_form': change_password_form
	}
	return render(request, 'account/profile.html', context=context)



@login_required
def get_address(request):
	if request.method == 'GET':
		id = request.GET.get('id')
		if not id:
			return JsonResponse({'success': False, 'message': 'Bad request'}, status=400)
		address = get_object_or_404(UserAddress, id=id, user=request.user.profile)
		response = {
			'id': id,
			'country': {'code': address.country.code, 'name': address.country.name},
			'region': address.region,
			'city': address.city,
			'street': address.street,
			'building_number': address.building_number,
			'block': address.block,
			'entrance': address.entrance,
			'appartment': address.appartment,
			'is_private_house': address.is_private_house,
			'zip_code': address.zip_code
		}
		return JsonResponse(response, status=200)
	return JsonResponse({'success': False, 'message': 'Method not allowed'}, status=405)