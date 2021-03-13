from django import forms

from .models import Order, OrderItem


class OrderForm(forms.ModelForm):
	is_billing_same = forms.BooleanField(required=False)

	class Meta:
		model = Order
		fields = ['billing_address', 'delivery_address', 'comment', 'is_billing_same']

	def clean(self):
		if self.cleaned_data.get('is_billing_same'):
			self.cleaned_data['billing_address'] = self.cleaned_data['delivery_address']
		return super(OrderForm, self).clean()
