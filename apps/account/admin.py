from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy as _

from apps.account.models import City

User = get_user_model()


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    fieldsets = (
        (None, {'fields': ('phone', 'password', 'is_corporate_account')}),
        (_('Personal info'), {'fields': (
            'first_name', 'last_name', 'avatar', 'tmp_phone', 'birth_date',
            'gender', 'active_point', 'inactive_point', 'discount', 'qr_code',
            'qr_code_updated_at', 'is_registration_finish', 'confirmation_code',
            'confirmation_date', 'user_1C_code'
        )}),
        (_('Permissions'), {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups',
                       'user_permissions'),
        }),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('phone', 'password1', 'password2'),
        }),
    )
    list_display = ('phone', 'first_name', 'last_name', 'is_superuser')
    list_filter = ('is_staff', 'is_superuser', 'is_active', 'groups')
    search_fields = ('phone', 'first_name', 'last_name')
    ordering = ('phone',)
    filter_horizontal = ('groups',)
    readonly_fields = (
        'phone', 'tmp_phone', 'active_point', 'qr_code_updated_at',
        'inactive_point', 'qr_code', 'user_1C_code', 'discount',
    )


@admin.register(City)
class CityAdmin(admin.ModelAdmin):
    pass
