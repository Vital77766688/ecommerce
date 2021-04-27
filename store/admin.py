from django.contrib import admin

from mptt.admin import MPTTModelAdmin

from .models import Category, Product


class CustomMPTTModelAdmin(MPTTModelAdmin):
	mptt_level_indent = 50


@admin.register(Category)
class CategoryAdmin(CustomMPTTModelAdmin):
	prepopulated_fields = {'category_slug': ('category_name',)}


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
	list_display = ('product_name', 'price', 'is_active')
	prepopulated_fields = {'product_slug': ('product_name',)}
