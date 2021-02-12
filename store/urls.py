from django.urls import path

from . import views

app_name = 'store'

urlpatterns = [
	path('', views.home, name='home'),
	path('store/<slug:slug>', views.category_list, name='category_list'),
	path('<slug:slug>', views.product_details, name='product_details'),
]
