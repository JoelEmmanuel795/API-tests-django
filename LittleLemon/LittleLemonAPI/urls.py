from django.urls import path
from . import views
from rest_framework.authtoken.views import obtain_auth_token

urlpatterns = [
    path('menu-items', views.MenuItemView.as_view(), name='menu-items'),
    path('menu-items/<int:pk>', views.SingleMenuItemView.as_view(), name='single-menu-item'),
    path('get-menu-items', views.get_menu_items, name='get-menu-items'),
    path('get-single-item/<int:id>', views.get_single_item, name='get-single-item'),
    path('get-taxed-items', views.get_taxed_items, name='get-taxed-items'),
    path('categories', views.get_categories, name='get-categories'),
    path('menu-items2',views.MenuItemsViewSet.as_view({'get':'list'})),
    path('menu-items2/<int:pk>',views.MenuItemsViewSet.as_view({'get':'retrieve'})),
    path('secret',views.secret,name='secret'),
    path('api-token-auth', obtain_auth_token, name='api_token_auth'),
    path('manager-view', views.manager_view, name='manager-view'),
    path('throttle-check', views.throttle_check, name='throttle-check'),
]