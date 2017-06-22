# -*- coding: utf-8 -*-
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin

from .models import User
from .forms import CreateUserForm, UserChangeForm

@admin.register(User)
class UserAdmin(DjangoUserAdmin):

    form = UserChangeForm
    add_form = CreateUserForm
    # don't need to override change_password_form

    list_display = ('username', 'is_superuser')
    list_filter = ()
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal info', {'fields': ('username',)}),
        ('Permissions', {'fields': ('is_superuser',)}),
    )
    # add_fieldsets is not a standard ModelAdmin attribute. UserAdmin
    # overrides get_fieldsets to use this attribute when creating a user.
    add_fieldsets = (
        (
            None,
            {
                'classes': ('wide',),
                'fields': ('username', 'password1', 'password2')
            }
        ),
    )
    search_fields = ('username',)
    ordering = ('username',)
    filter_horizontal = ()
