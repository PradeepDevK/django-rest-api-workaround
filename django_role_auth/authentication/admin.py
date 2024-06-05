from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User

class CustomUserAdmin(UserAdmin):
    # Add the `role` field to the fieldsets to include it on the user detail page
    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('role',)}),
    )

    # Add the `role` field to the add_fieldsets to include it on the user creation page
    add_fieldsets = UserAdmin.add_fieldsets + (
        (None, {'fields': ('role',)}),
    )

    # Optionally, you can add the `role` field to the list_display to include it in the user list view
    list_display = UserAdmin.list_display + ('role',)

admin.site.register(User, CustomUserAdmin)