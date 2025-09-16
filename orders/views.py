from decimal import Decimal
from django.http import HttpRequest, HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST
from events.models import TicketType
from .services import checkout as checkout_service

CART_SESSION_KEY = 'cart'

def _get_cart(session):
    cart = session.get(CART_SESSION_KEY)
    if cart is None:
        cart = {}
        session[CART_SESSION_KEY] = cart
    return cart


@require_POST
def add_to_cart(request: HttpRequest) -> HttpResponse:
    ticket_type_id = request.POST.get('ticket_type_id')
    quantity_raw = request.POST.get('quantity', '1')
    try:
        quantity = max(int(quantity_raw), 1)
    except (TypeError, ValueError):
        quantity = 1

    ticket_type = get_object_or_404(TicketType, pk=ticket_type_id, active=True)
    
    if ticket_type.available <= 0:
        return _redirect_with_message(request, 'orders:cart_view', False, f"{ticket_type.name} está agotado")

    cart = _get_cart(request.session)
    item = cart.get(str(ticket_type.id))

    if item:
        new_qty = item['quantity'] + quantity
        if new_qty > ticket_type.available:
            new_qty = ticket_type.available
        item['quantity'] = new_qty
    else:
        cart[str(ticket_type.id)] = {
            'ticket_type_id': ticket_type.id,
            'event_id': ticket_type.event_id,
            'name': ticket_type.name,
            'price': str(ticket_type.price),
            'quantity': min(quantity, ticket_type.available),
        }

    request.session.modified = True

    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return JsonResponse({'ok': True, 'cart_count': _cart_total_quantity(cart)})
    return redirect('orders:cart_view')


@require_POST
def remove_from_cart(request: HttpRequest) -> HttpResponse:
    ticket_type_id = request.POST.get('ticket_type_id')
    cart = _get_cart(request.session)
    if ticket_type_id and str(ticket_type_id) in cart:
        del cart[str(ticket_type_id)]
        request.session.modified = True
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return JsonResponse({'ok': True, 'cart_count': _cart_total_quantity(cart)})
    return redirect('orders:cart_view')


def cart_view(request: HttpRequest) -> HttpResponse:
    cart = _get_cart(request.session)
    items = []
    total = Decimal('0.00')
    for key, data in cart.items():
        price = Decimal(data['price'])
        quantity = int(data['quantity'])
        line_total = price * quantity
        total += line_total
        items.append({
            **data,
            'price': price,
            'line_total': line_total,
        })
    context = {
        'items': items,
        'total': total,
    }
    return render(request, 'orders/cart.html', context)


def _cart_total_quantity(cart: dict) -> int:
    return sum(int(v.get('quantity', 0)) for v in cart.values())


def checkout_view(request: HttpRequest) -> HttpResponse:
    cart = request.session.get(CART_SESSION_KEY, {})
    if request.method == 'POST':
        try:
            order = checkout_service(cart, user=request.user if request.user.is_authenticated else None)
        except Exception as exc:
            return render(request, 'orders/checkout.html', {
                'error': str(exc),
                'cart': cart,
            })
        # limpiar carrito
        request.session[CART_SESSION_KEY] = {}
        request.session.modified = True
        return render(request, 'orders/checkout.html', {
            'order': order,
            'success': True,
        })
    return render(request, 'orders/checkout.html', {
        'cart': cart,
    })


@require_POST
def update_quantity(request: HttpRequest) -> HttpResponse:
    ticket_type_id = request.POST.get('ticket_type_id')
    delta_raw = request.POST.get('delta')
    if ticket_type_id is None or delta_raw not in {'+1', '-1'}:
        return redirect('orders:cart_view')

    cart = _get_cart(request.session)
    item = cart.get(str(ticket_type_id))
    if not item:
        return redirect('orders:cart_view')

    tt = get_object_or_404(TicketType, pk=ticket_type_id, active=True)
    current_qty = int(item['quantity'])
    delta = 1 if delta_raw == '+1' else -1
    new_qty = current_qty + delta
    if new_qty < 1:
        del cart[str(ticket_type_id)]
    else:
        if new_qty > tt.available:
            new_qty = tt.available
        item['quantity'] = new_qty

    request.session.modified = True
    return redirect('orders:cart_view')


def _redirect_with_message(request: HttpRequest, to: str, success: bool, message: str) -> HttpResponse:
    from django.contrib import messages
    (messages.success if success else messages.error)(request, message)
    return redirect(to)

