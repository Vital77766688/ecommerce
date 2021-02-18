from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import User


class UserAdmin(UserAdmin):
	model = User
	list_display = ('email', 'is_staff', 'is_email_verified', 'is_active',)
	list_filter = ('email', 'is_staff', 'is_active')
	filter_horizontal = ()
	fieldsets = (
		('General Info', {'fields': ('email', 'is_email_verified')}),
		('Permissions', {'fields': ('is_staff', 'is_active', 'is_superuser')})
	)
	add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2', 'is_staff', 'is_active')}
        ),
    )
	ordering = ()


admin.site.register(User, UserAdmin)