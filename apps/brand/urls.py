from django.urls import path, include

from apps.brand.views import (
    BrandRetrieveAPIView, BrandListAPIView, FilialListAPIView,
    FilialRetrieveAPIView
)


urlpatterns = [
    path('', BrandListAPIView.as_view(), name='brand_list'),
    path('<int:id>/', BrandRetrieveAPIView.as_view(), name='brand_detail'),
    path('filial/', include([
        path('', FilialListAPIView.as_view(), name='filial_list'),
        path('<int:id>/', FilialRetrieveAPIView.as_view(), name='filial_detail')
    ])),
]
