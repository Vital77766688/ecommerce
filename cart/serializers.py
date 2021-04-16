from django.shortcuts import get_object_or_404

from rest_framework import serializers

from .cart import Cart
from store.models import Product


class CartSerializer(serializers.Serializer):
	id = serializers.IntegerField()
	qty = serializers.IntegerField()

	def create(self, validated_data):
		cart = Cart(self.context['request'])
		id, price = validated_data['id']
		qty = validated_data['qty']
		self.message = cart.update(id, price, qty)
		return len(cart)

	def validate_id(self, value):
		product = get_object_or_404(Product, pk=value)
		return (str(product.id), str(product.price))

	def to_representation(self, instance):
		return {'success': True, 
				'message': self.message, 
				'data': {'cart_qty': instance}
				}