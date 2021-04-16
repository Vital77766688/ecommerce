from django.urls import path

from . import api

app_name = 'cart_api'

urlpatterns = [
	path('update_cart/', api.UpdateCartView.as_view(), name='update_cart'),
]