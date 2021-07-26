from django.urls import path

from .views import (
    BannerAndPromotionAPIView,
    BannerRetrieveAPIView,
    ProgramConditionAPIView,
    ContactListAPIView,
    PromotionAndNewsListAPIView,
    PromotionAndNewsRetrieveAPIView,
)

urlpatterns = [
    path(
        'promotions-news/',
        PromotionAndNewsListAPIView.as_view(),
        name='promotions-news'
    ),
    path(
        'promotions-news/<int:pk>/',
        PromotionAndNewsRetrieveAPIView.as_view(),
        name='promotions-news-detail'
    ),
    path(
        'banner-promotions/',
        BannerAndPromotionAPIView.as_view(),
        name='banner-promotions'
    ),
    path(
        'banner/',
        BannerRetrieveAPIView.as_view(),
        name='banner-detail'
    ),
    path(
        'program-condition/',
        ProgramConditionAPIView.as_view(),
        name='program_condition'
    ),
    path('contacts/', ContactListAPIView.as_view(), name='contacts')
]
