from django.contrib import admin

from solo.admin import SingletonModelAdmin

from apps.setting.models import Setting, AppVersion, HelpPage


@admin.register(Setting)
class SettingAdmin(SingletonModelAdmin):
    pass


@admin.register(HelpPage)
class HelpPageAdmin(SingletonModelAdmin):
    pass


@admin.register(AppVersion)
class AppVersionAdmin(SingletonModelAdmin):
    fieldsets = (
        ('Android', {
            'fields': (
                'android_version',
                'android_force_update',
            )
        }),
        ('Ios', {
            'fields': (
                'ios_build_number',
                'ios_version',
                'ios_force_update',
            )
        })
    )
