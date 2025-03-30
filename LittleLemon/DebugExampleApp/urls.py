from . import views
from django.urls import path

urlpatterns = [
    path('even_numbers/', views.display_even_numbers, name='display_even_numbers'),
]