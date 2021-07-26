from django.contrib import admin

from apps.check.models import Check


@admin.register(Check)
class CheckAdmin(admin.ModelAdmin):
    list_display = ('unique_1c_check_code', 'user', 'filial',)
    search_fields = ('unique_1c_check_code',)
    readonly_fields = (
        'unique_1c_check_code', 'money_paid', 'bonus_paid', 'total_paid',
        'accrued_point', 'accrued_point_date', 'withdrawn_point',
        'withdrawn_point_date', 'is_active', 'user', 'filial', 'status',
        'is_on_credit', 'balance_owed', 'due_date',
    )
    exclude = (
        'user_1c_code', 'filial_1c_code'
    )

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False
