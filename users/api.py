from django.shortcuts import get_object_or_404

from rest_framework import status
from rest_framework.generics import RetrieveAPIView
from rest_framework.response import Response

from .serializers import UserAddressSerializer
from .models import UserAddress


class UserAddressView(RetrieveAPIView):
	serializer_class = UserAddressSerializer

	def get_object(self):
		queryset = self.filter_queryset(self.get_queryset())

		id = self.request.query_params.get('id')
		obj = get_object_or_404(queryset, pk=id)
		self.check_object_permissions(self.request, obj)

		return obj

	def get_queryset(self):
		return UserAddress.objects.filter(user=self.request.user.profile)