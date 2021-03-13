from django.urls import path

from . import views

app_name = 'users'

urlpatterns = [
	path('profile/', views.profile, name='profile'),
	path('api/get_address/', views.get_address, name='address'),
]
