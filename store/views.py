from django.http import Http404
from django.shortcuts import get_object_or_404, render
from django.core.paginator import Paginator, InvalidPage
from django.utils.translation import gettext_lazy as _

from . models import Category, Product


def home(request):
	try:
		page_number = request.GET.get('page') or 1
		limit_per_page = request.GET.get('limit') or 15

		page_number = int(page_number)
		limit_per_page = int(limit_per_page)

		if limit_per_page > 100: limit_per_page = 3

		page = Paginator(Product.objects.all(), limit_per_page).page(page_number)
	except InvalidPage:
		raise Http404(_("Page does not exists"))

	context = {
		'products': page,
		'current_page': page.number,
		'page_range': page.paginator.page_range,
		'is_paginated': page.has_other_pages(),
		'previous_page': page.previous_page_number() if page.has_previous() else None,
		'next_page': page.next_page_number() if page.has_next() else None,
		'total_pages': page.paginator.num_pages,
	}
	return render(request, 'store/home.html', context=context)


def category_list(request, slug):
	if slug == 'all':
		category = Category(category_name='All', category_slug='all')
		products = Product.objects.all()
	else:
		category = get_object_or_404(Category, category_slug=slug)
		products = Product.objects.filter(category=category)

	try:
		page_number = request.GET.get('page') or 1
		limit_per_page = request.GET.get('limit') or 15

		page_number = int(page_number)
		limit_per_page = int(limit_per_page)

		if limit_per_page > 100: limit_per_page = 3

		page = Paginator(products, limit_per_page).page(page_number)
	except InvalidPage:
		raise Http404(_("Page does not exists"))

	context = {
		'category': category,
		'products': page,
		'current_page': page.number,
		'page_range': page.paginator.page_range,
		'is_paginated': page.has_other_pages(),
		'previous_page': page.previous_page_number() if page.has_previous() else None,
		'next_page': page.next_page_number() if page.has_next() else None,
		'total_pages': page.paginator.num_pages,
	}
	
	return render(request, 'store/category_list.html', context=context)


def product_details(request, slug):
	product = get_object_or_404(Product, product_slug=slug)
	context = {'product': product}
	return render(request, 'store/product_details.html', context=context)