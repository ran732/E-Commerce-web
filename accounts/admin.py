from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Account


class AccountAdmin(UserAdmin):

    list_display = [
        'email',
        'first_name',
        'username',
        'last_name',
        'date_joined',
        'is_active'
    ]

    list_display_links = (
        'email',
        'first_name',
        'username',
        'last_name'
    )

    readonly_fields = (
        'last_login',
        'date_joined'
    )

    ordering = ('-date_joined',)

    filter_horizontal = ()
    list_filter = ()

    fieldsets = (
        ('Personal Information', {
            'fields': (
                'first_name',
                'last_name',
                'username',
                'email',
                'phone_number',
                'password',
            )
        }),

        ('Permissions', {
            'fields': (
                'is_active',
                'is_staff',
                'is_admin',
                'is_superadmin',
            )
        }),

        ('Important Dates', {
            'fields': (
                'last_login',
                'date_joined',
            )
        }),
    )




admin.site.register(Account, AccountAdmin)