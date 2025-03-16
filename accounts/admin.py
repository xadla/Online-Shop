from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import Group


from .models import User
from .forms import UserCreationForm, UserChangeForm


class UserAdmin(BaseUserAdmin):

    form =  UserChangeForm
    add_form = UserCreationForm


    list_display = ["email", "is_admin", "phone_number"]
    list_filter = ["is_admin"]

    fieldsets = [
        (None, {"fields": ["email", "password"]}),
        ("Information", {"fields": ["first_name", "last_name", "address", "phone_number", "last_login"]}),
        ("Permission", {"fields": ["is_admin"]})
    ]

    add_fieldsets = [
        (
            None,
            {
                "fields": ["email", "first_name", "last_name", "password1", "password2"],
            },
        )
    ]

    search_fields = ["email"]
    ordering = ["email"]
    filter_horizontal = []


admin.site.register(User, UserAdmin)
admin.site.unregister(Group)