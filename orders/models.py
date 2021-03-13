from django.utils.translation import gettext_lazy as _
from django.db import models
from django.core.mail import send_mail

from store.models import Product
from users.models import UserAddress, UserProfile



class OrderStatus(models.Model):
	status_name = models.CharField(_('Order status'), max_length=50)

	def __str__(self):
		return self.status_name

	class Meta:
		verbose_name = _('Order status')
		verbose_name_plural = _('Order statuses')
		db_table = 'order_status'


class Order(models.Model):
	user = models.ForeignKey(UserProfile, on_delete=models.RESTRICT, related_name='orders')
	delivery_address = models.ForeignKey(UserAddress, on_delete=models.RESTRICT, related_name='orders_d')
	billing_address = models.ForeignKey(UserAddress, on_delete=models.RESTRICT, related_name='orders_b')
	status = models.ForeignKey(OrderStatus, on_delete=models.RESTRICT, default=1)
	price = models.DecimalField(_('Order price'), max_digits=10, decimal_places=2)
	comment = models.TextField(_('Comment'), null=True, blank=True)
	create_date = models.DateTimeField(_('Create date'), auto_now_add=True)
	update_date = models.DateTimeField(_('Update date'), auto_now=True)


	def __str__(self):
		return f"{self.user.user.email}: {self.pk}"

	def save(self, cart=None, *args, **kwargs):
		super(Order, self).save()
		if cart:
			for item in cart:
				OrderItem.objects.create(
					order=self,
					product = item['product'],
					price = item['product'].price,
					qty = item['qty']
				)
			cart.clean()

	class Meta:
		verbose_name = _('Order')
		verbose_name_plural = _('Orders')
		db_table = 'orders'
		ordering = ('-create_date',)


class OrderItem(models.Model):
	order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
	product = models.ForeignKey(Product, on_delete=models.RESTRICT)
	price = models.DecimalField(_('Price'), max_digits=10, decimal_places=2)
	qty = models.IntegerField()

	def __str__(self):
		return f"{self.order.pk}: {self.product.product_name}"

	class Meta:
		verbose_name = _('Order item')
		verbose_name_plural = _('Order items')
		db_table = 'order_items'