def update_cart(request, ticket_type_id):
    if request.method == "POST":
        cart = request.session.get('cart', {})
        ticket = get_object_or_404(TicketType, id=ticket_type_id, active=True)
        try:
            quantity = int(request.POST.get('quantity', 1))
        except (TypeError, ValueError):
            quantity = 1
        if quantity < 1:
            quantity = 1
        if quantity > ticket.remaining:
            quantity = ticket.remaining
        item = cart.get(str(ticket.id), {"quantity": 0})
        item["quantity"] = quantity
        cart[str(ticket.id)] = item
        request.session['cart'] = cart
    return redirect('orders:cart_view')
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from events.models import TicketType
from .services import checkout, NotEnoughTickets
from payments.adapters.dummy import DummyPaymentGateway
from .models import Order


def add_to_cart(request, ticket_type_id):
    cart = request.session.get('cart', {})
    ticket = get_object_or_404(TicketType, id=ticket_type_id, active=True)

    # Obtener la cantidad del formulario POST, por defecto 1
    try:
        quantity = int(request.POST.get('quantity', 1))
    except (TypeError, ValueError):
        quantity = 1

    # usamos str(id) porque las claves de sesión deben ser serializables
    item = cart.get(str(ticket.id), {"quantity": 0})
    item["quantity"] += quantity
    cart[str(ticket.id)] = item

    request.session['cart'] = cart
    return redirect('orders:cart_view')


def remove_from_cart(request, ticket_type_id):
    cart = request.session.get('cart', {})
    ticket_id = str(ticket_type_id)
    if ticket_id in cart:
        del cart[ticket_id]
        request.session['cart'] = cart
    return redirect('orders:cart_view')


def cart_view(request):
    cart = request.session.get('cart', {})
    items = []
    total = 0

    for ticket_id, item in cart.items():
        ticket = TicketType.objects.get(id=ticket_id)
        quantity = item["quantity"]
        subtotal = ticket.price * quantity
        total += subtotal
        items.append({
            "ticket": ticket,
            "quantity": quantity,
            "subtotal": subtotal,
        })

    return render(request, "orders/cart.html", {"items": items, "total": total})


def checkout_view(request):
    cart = request.session.get('cart', {})
    order = None
    error = None

    if request.method == "POST":
        try:
            gateway = DummyPaymentGateway()
            order = checkout(cart, gateway)
            if order.status == "paid":
                request.session['cart'] = {}  # vaciar carrito al pagar
                return redirect("orders:order_success", order_id=order.id)
        except NotEnoughTickets as e:
            error = str(e)

    return render(request, "orders/checkout.html", {"cart": cart, "order": order, "error": error})



def order_success(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    return render(request, "orders/order_success.html", {"order": order})


def order_detail(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    return render(request, "orders/order_detail.html", {"order": order})
