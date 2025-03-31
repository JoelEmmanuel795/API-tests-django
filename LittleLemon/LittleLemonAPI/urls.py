from django.urls import path
from . import views

urlpatterns = [
    path('menu-items', views.MenuItemView.as_view(), name='menu-items'),
    path('menu-items/<int:pk>', views.SingleMenuItemView.as_view(), name='single-menu-item'),
    path('get-menu-items', views.get_menu_items, name='get-menu-items'),
    path('get-single-item/<int:id>', views.get_single_item, name='get-single-item'),
]