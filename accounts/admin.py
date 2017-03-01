# coding: utf8
from .forms import AdminUserChangeForm, AdminUserAddForm
from accounts.models import User, UserProfile
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import ugettext_lazy as _


# Указываем наши форма для создания и редактирования пользователя.
# Добавляем новые поля в fieldsets, и поле email в add_fieldsets.
class UserAdmin(BaseUserAdmin):
    form = AdminUserChangeForm
    add_form = AdminUserAddForm
    list_display = ('pk', 'username')
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        (_('Personal info'), {'fields': (
            'first_name',
            'last_name',
            'email',
            'avatar',
            'birthday',
            'phone_number',
            'city',
            'adress',
            'passWallet',
            'structure',
            'active_is_structure',
            'parent'
        )}),
        (_('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser',
                                       'groups', 'user_permissions')}),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'password1', 'password2')}
        )
    )

admin.site.register(User, UserAdmin)


admin.site.register(UserProfile)

