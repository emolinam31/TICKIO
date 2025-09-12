from django.shortcuts import render, redirect, get_object_or_404
from events.models import TicketType

def add_to_cart(request, ticket_type_id):
    cart = request.session.get('cart', {})

    ticket = get_object_or_404(TicketType, id=ticket_type_id, active=True)

    # usamos str(id) porque las claves de sesión deben ser serializables
    item = cart.get(str(ticket.id), {"quantity": 0})
    item["quantity"] += 1
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
