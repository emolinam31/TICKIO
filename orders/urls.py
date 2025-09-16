from django.urls import path
from . import views

app_name = 'orders'

urlpatterns = [
    path('add/', views.add_to_cart, name='add_to_cart'),
    path('remove/', views.remove_from_cart, name='remove_from_cart'),
    path('update/', views.update_quantity, name='update_quantity'),
    path('cart/', views.cart_view, name='cart_view'),
    path('checkout/', views.checkout_view, name='checkout'),
]


