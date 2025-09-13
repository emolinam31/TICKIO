from django.urls import path
from . import views

app_name = "orders"

urlpatterns = [
    path("add/<int:ticket_type_id>/", views.add_to_cart, name="add_to_cart"),
    path("remove/<int:ticket_type_id>/", views.remove_from_cart, name="remove_from_cart"),
    path("cart/", views.cart_view, name="cart_view"),
    path("checkout/", views.checkout_view, name="checkout"),
    path("success/<int:order_id>/", views.order_success, name="order_success"),  
]
