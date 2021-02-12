from django.contrib import admin

from .models import Category, Product


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
	prepopulated_fields = {'category_slug': ('category_name',)}


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
	list_display = ('product_name', 'price', 'is_active')
	prepopulated_fields = {'product_slug': ('product_name',)}
