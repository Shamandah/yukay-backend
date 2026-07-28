from django.urls import path
from .views import (
    CategoryListAPIView,
    MenuItemListAPIView,
)


urlpatterns = [
    path(
        "categories/",
        CategoryListAPIView.as_view(),
        name="categories"
    ),

    path(
        "menu/",
        MenuItemListAPIView.as_view(),
        name="menu-items"
    ),
]