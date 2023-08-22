from django.contrib import admin
from app_auth.models import User
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

# Register your models here.


class UserAdminModel(BaseUserAdmin):
    # The fields to be used in displaying the User model.
    # These override the definitions on the base UserAdminModel
    # that reference specific fields on auth.User.
    list_display = ["id", "name", "email", "phone", "is_active", "is_admin"]
    list_filter = ["is_admin"]
    fieldsets = [
        ("User Credentials", {"fields": ["email", "password"]}),
        ("Personal info", {"fields": ["name", "phone"]}),
        ("Permissions", {"fields": ["is_admin"]}),
    ]
    # add_fieldsets is not a standard ModelAdmin attribute. UserAdminModel
    # overrides get_fieldsets to use this attribute when creating a user.
    add_fieldsets = [
        (
            None,
            {
                "classes": ["wide"],
                "fields": ["name", "email", "phone", "password1", "password2"],
            },
        ),
    ]
    search_fields = ["email"]
    ordering = ["email", "id"]
    filter_horizontal = []


# Now register the new UserAdminModel...
admin.site.register(User, UserAdminModel)
