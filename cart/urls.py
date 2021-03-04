from django.urls import path

from . import views

app_name = 'cart'

urlpatterns = [
	path('', views.cart_summary, name='cart_summary'),
	path('update_cart/', views.update_cart, name='update_cart'),
]
