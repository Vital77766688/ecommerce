from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
	path('', include('store.urls', namespace='store')),
	path('cart/', include('cart.urls', namespace='cart')),
	path('orders/', include('orders.urls', namespace='orders')),
	path('accounts/', include('allauth.urls')),
	path('accounts/', include('users.urls')),
    path('admin/', admin.site.urls),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)