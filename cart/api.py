from rest_framework.mixins import CreateModelMixin, DestroyModelMixin
from rest_framework.generics import GenericAPIView

from .cart import Cart
from .serializers import CartSerializer


class UpdateCartView(CreateModelMixin, DestroyModelMixin, GenericAPIView):
	serializer_class = CartSerializer

	def get_object(self):
		return Cart(self.request)

	def post(self, request, *args, **kwargs):
		return self.create(request, *args, **kwargs)

	def delete(self, request, *args, **kwargs):
		return self.destroy(request, *args, **kwargs)

	def perform_destroy(self, instance):
		if self.request.data.get('id'):
			instance.delete(self.request.data['id'])
