from django.contrib import admin

from solo.admin import SingletonModelAdmin

from apps.brand.admin import ImageInlineFormSet
from .models import (
    Banner, ProgramCondition, Contact,
    PromotionAndNews, PromotionAndNewsImage, ContactIcon,
)
from apps.notifications.tasks import save_notification_and_send_fcm_for_article


class PromotionAndNewsImageInline(admin.StackedInline):
    model = PromotionAndNewsImage
    extra = 0
    formset = ImageInlineFormSet


@admin.register(Banner)
class BannerAdmin(SingletonModelAdmin):
    list_display = ('title',)


@admin.register(ProgramCondition)
class ProgramConditionAdmin(SingletonModelAdmin):
    list_display = ('title', 'description',)


@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ('title', 'icon_image', 'link',)


@admin.register(ContactIcon)
class ContactIconAdmin(admin.ModelAdmin):
    pass


@admin.register(PromotionAndNews)
class PromotionAndNewsAdmin(admin.ModelAdmin):
    list_display = ('title', 'information_type', 'is_active',)
    fields = [
            'created_at', 'title', 'description',
            'information_type', 'is_active',
        ]
    inlines = (PromotionAndNewsImageInline,)

    def save_model(self, request, obj, form, change):
        is_old = obj.pk   # checking for existence in the database
        super().save_model(request, obj, form, change)
        if not is_old:
            if obj.is_active:
                body = {
                    'object_id': obj.id,
                    'title': obj.title,
                    'information_type': obj.information_type,
                }
                save_notification_and_send_fcm_for_article(body, obj)
