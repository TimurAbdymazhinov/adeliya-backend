from django.conf import settings
from django.conf.urls import url
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include, re_path

from drf_yasg import openapi
from drf_yasg.views import get_schema_view

admin.site.site_header = "Adeliya"
admin.site.site_title = "Adeliya"
admin.site.index_title = "Админ-панель Adeliya"


schema_view = get_schema_view(
   openapi.Info(
      title="Adeliya API",
      default_version='v1',
      description="Adeliya API description",
      terms_of_service="https://www.google.com/policies/terms/",
      contact=openapi.Contact(email="kalmanbetovaman@gmail.com"),
      license=openapi.License(name="BSD License"),
   ),
   public=True,
   permission_classes=(settings.API_PERMISSION,),
)

v1_api = ([
    path('account/', include('apps.account.urls')),
    path('brand/', include('apps.brand.urls')),
    path('info/', include('apps.info.urls')),
    path('check/', include('apps.check.urls')),
    path('notification/', include('apps.notifications.urls')),
    path('setting/', include('apps.setting.urls')),
    path('1c/', include('apps.integration.urls'))
], 'v1')

urlpatterns = [
    path('jet/', include('jet.urls', 'jet')),
    path('admin/', admin.site.urls),
    path('ckeditor/', include('ckeditor_uploader.urls')),

    url(r'^docs(?P<format>\.json|\.yaml)$',
        schema_view.without_ui(cache_timeout=0), name='schema-json'),
    url(r'^docs/$', schema_view.with_ui('swagger', cache_timeout=0),
        name='schema-swagger-ui'),
    url(r'^redocs/$', schema_view.with_ui('redoc', cache_timeout=0),
        name='schema-redoc'),

    re_path(r'api/v1/', include(v1_api, namespace='v1')),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    import debug_toolbar
    urlpatterns += [path('__debug__/', include(debug_toolbar.urls))]
