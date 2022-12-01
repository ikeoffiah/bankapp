from django.contrib import admin
from .models import User
from django.contrib.auth.admin import UserAdmin


class UserAdminConfig(UserAdmin):
    search_fields = ('email', 'first_name', 'last_name')
    list_display = (
    'email', 'first_name', 'last_name', 'is_staff', 'is_active', 'date_joined', 'last_login')
    list_filter = ('email', 'first_name', 'last_name', )
    ordering = ('-date_joined',)
    fieldsets = (
        (None, {'fields': ('email','first_name', 'last_name')}),
        ('Permissions', {'fields': ('is_staff', 'is_active')})

    )
    add_fieldsets = (

        None, {'classes': ('wide'),
               'fields': ('email', 'first_name', 'last_name', 'is_staff', 'is_active', 'last_login')}
    )


admin.site.register(User, UserAdminConfig)


