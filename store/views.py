from django.shortcuts import get_object_or_404, render

from . models import Category, Product


def home(request):
	context = {'products': Product.objects.all()}
	return render(request, 'store/home.html', context=context)


def category_list(request, slug):
	if slug == 'all':
		category = Category(category_name='All', category_slug='all')
		products = Product.objects.all()
	else:
		category = get_object_or_404(Category, category_slug=slug)
		products = Product.objects.filter(category=category)

	context = {
		'category': category,
		'products': products
	}
	return render(request, 'store/category_list.html', context=context)


def product_details(request, slug):
	product = get_object_or_404(Product, product_slug=slug)
	context = {'product': product}
	return render(request, 'store/product_details.html', context=context)