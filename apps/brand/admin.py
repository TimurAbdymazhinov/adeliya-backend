from django.contrib import admin
from django.forms.models import BaseInlineFormSet

from adminsortable2.admin import SortableAdminMixin
from django_2gis_maps.admin import DoubleGisAdmin

from apps.brand.models import (
    Brand, BrandImage, Filial, FilialImage, FilialPhone, WorkTime
)
from apps.brand.service import WorkDayService


class ImageInlineFormSet(BaseInlineFormSet):
    """
    This formset class is for check main image count
    max count of main image is equal to 1
    """
    def clean(self):
        super(ImageInlineFormSet, self).clean()
        main_photo_count = 0
        for form in self.forms:
            is_main_image = (
                form.cleaned_data and not form.cleaned_data.get('DELETE') and
                form.cleaned_data['is_main']
            )

            if is_main_image:
                main_photo_count += 1

            if main_photo_count > 1 and form.cleaned_data['is_main']:
                form.add_error(
                    'is_main',
                    'Допускается только одно изображение, как основное'
                )

        if self.forms and not main_photo_count:
            self.forms[0].add_error(
                'is_main',
                'Хотя бы одно изображение должно быть, как основное'
            )


class NumberInlineFormSet(BaseInlineFormSet):
    """
    This formset class is for check number
    """
    def clean(self):
        super(NumberInlineFormSet, self).clean()
        for form in self.forms:
            is_valid_number_object = (
                form.cleaned_data and not form.cleaned_data.get('DELETE') and (
                    form.cleaned_data['is_phone'] or
                    form.cleaned_data['is_whatsapp']
                )
            )

            if not is_valid_number_object:
                form.add_error(
                    'is_phone',
                    'У номера должна быть включена хотя бы одна функция'
                )
                form.add_error(
                    'is_whatsapp',
                    'У номера должна быть включена хотя бы одна функция'
                )


class WorkTimeInline(admin.TabularInline):
    model = WorkTime
    can_delete = False
    fields = ['day', 'start_work', 'end_work']
    readonly_fields = ['day']

    def has_add_permission(self, request, obj=None):
        return False


class BrandImageAdmin(admin.TabularInline):
    model = BrandImage
    extra = 0


@admin.register(Brand)
class BrandAdmin(SortableAdminMixin, admin.ModelAdmin):
    inlines = (BrandImageAdmin,)
    list_display = ('position', 'title', 'address', 'link',)
    list_display_links = ['title']
    search_fields = ['title']


class FilialImageAdmin(admin.TabularInline):
    model = FilialImage
    extra = 0
    formset = ImageInlineFormSet


class FilialPhoneAdmin(admin.TabularInline):
    model = FilialPhone
    extra = 0
    formset = NumberInlineFormSet


@admin.register(Filial)
class FilialAdmin(SortableAdminMixin, DoubleGisAdmin):
    inlines = (FilialImageAdmin, FilialPhoneAdmin, WorkTimeInline)
    list_display = ('position', 'title', 'address',)
    list_display_links = ['title']
    search_fields = ['title']

    def get_inline_instances(self, request, obj=None):
        inline_instances = []
        try:
            work_time_obj = obj.works_time.all()
            if work_time_obj:
                pass
            else:
                WorkDayService.create_weekday(obj)

        except Exception:
            pass

        for inline_class in self.inlines:
            inline = inline_class(self.model, self.admin_site)
            if request:
                inline_has_add_permission = inline._has_add_permission(request,
                                                                       obj)
                if not (inline.has_view_or_change_permission(request, obj) or
                        inline_has_add_permission or
                        inline.has_delete_permission(request, obj)):
                    continue
                if not inline_has_add_permission:
                    inline.max_num = 0
            inline_instances.append(inline)

        return inline_instances





