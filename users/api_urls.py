from django.urls import path

from . import api

app_name = 'users_api'

urlpatterns = [
	path('get_address/', api.UserAddressView.as_view(), name='address'),
]