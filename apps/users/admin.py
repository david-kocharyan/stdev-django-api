from django.contrib import admin
from django.contrib.auth.models import Group
from django.contrib.auth import admin as auth_admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from rest_framework_simplejwt.token_blacklist import admin as jwt_admin
from rest_framework_simplejwt.token_blacklist import models as jwt_models

from apps.users.models import User


class UserAdmin(BaseUserAdmin):
    model = User

    list_display = ('email', 'first_name', 'last_name', 'is_active', 'created_at')
    search_fields = ('name', 'email', 'first_name', 'last_name')
    ordering = ('-created_at',)
    change_password_form = auth_admin.AdminPasswordChangeForm

    fieldsets = (
        ('Personal Info', {'fields': ('email', 'first_name', 'last_name', 'password', 'image', 'is_active')}),
        ('Other info', {'fields': ('last_login', 'created_at', 'updated_at')}),
    )
    readonly_fields = ('created_at', 'updated_at', 'last_login')

    def has_add_permission(self, request):
        return False


class OutstandingTokenAdmin(jwt_admin.OutstandingTokenAdmin):
    def has_delete_permission(self, *args, **kwargs):
        return True


admin.site.unregister(jwt_models.OutstandingToken)
admin.site.register(jwt_models.OutstandingToken, OutstandingTokenAdmin)

admin.site.register(User, UserAdmin)
admin.site.unregister(Group)
