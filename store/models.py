from datetime import datetime

from django.utils.translation import gettext_lazy as _
from django.db import models

from PIL import Image


def image_path(instance, filename):
	ext = filename.split('.')[-1]
	return f"images/products/{instance.id}_{datetime.now().strftime('%Y%m%s%H%M%S')}.{ext}"


class Category(models.Model):
	category_name = models.CharField(max_length=50, db_index=True, verbose_name=_('Name'))
	category_slug = models.SlugField(max_length=50, unique=True)

	def __str__(self):
		return self.category_name

	class Meta:
		verbose_name = _('Category')
		verbose_name_plural = _('Categories')
		db_table = 'categories'


class Product(models.Model):
	category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, related_name='product')
	product_name = models.CharField(max_length=50, verbose_name=_('Name'))
	product_slug = models.SlugField(max_length=50, unique=True)
	price = models.DecimalField(max_digits=10, decimal_places=2)
	image = models.ImageField(upload_to=image_path, default='images/product_default.jpeg')
	description = models.TextField(blank=True, null=True)
	is_active = models.BooleanField(default=True)
	created_at = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return self.product_name

	class Meta:
		verbose_name = 'Product'
		verbose_name_plural = 'Products'
		db_table = 'products'
		ordering = ('-created_at',)

	def save(self, *args, **kwargs):
		super().save(*args, **kwargs)

		img = Image.open(self.image.path)

		if img.height > 300 or img.width > 300:
			output_size = (300, 300)
			img.thumbnail(output_size)
			img.save(self.image.path)