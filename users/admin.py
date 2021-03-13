from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import User, UserProfile, UserAddress


class UserAdmin(UserAdmin):
	model = User
	list_display = ('email', 'is_staff', 'is_active',)
	list_filter = ('email', 'is_staff', 'is_active')
	filter_horizontal = ()
	fieldsets = (
		('General Info', {'fields': ('email',)}),
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


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
	pass


@admin.register(UserAddress)
class UserAddressAdmin(admin.ModelAdmin):
	pass
