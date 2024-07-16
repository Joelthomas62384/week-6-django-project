from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User  # Change this line to match your model name

class CustomUserAdmin(UserAdmin):
    model = User

    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('email_verified',)}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        (None, {'fields': ('email_verified',)}),
    )

admin.site.register(User, CustomUserAdmin)
