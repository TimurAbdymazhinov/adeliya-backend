from django.contrib import admin

from apps.notifications.models import Notification


@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ['__str__', 'notice_type', 'user', 'is_viewed', 'is_active']
    list_filter = ['user', 'notice_type', 'is_active']
    fields = [
        'user', 'notice_type', 'linked_check', 'linked_article',
        'is_viewed', 'is_active', 'is_on_credit',
    ]
    readonly_fields = [
        'user', 'notice_type', 'linked_check', 'linked_article',
        'is_viewed', 'is_active', 'is_on_credit',
    ]
