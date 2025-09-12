from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Order, Ticket
from events.models import Event
from django.db import transaction

@login_required
def my_orders(request):
    orders = Order.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'orders/my_orders.html', {'orders': orders})

@login_required
def ticket_detail(request, ticket_id):
    ticket = get_object_or_404(Ticket, ticket_id=ticket_id, user=request.user)
    return render(request, 'orders/ticket_detail.html', {'ticket': ticket})

# This is a placeholder view to simulate an order creation.
# In a real app, this would be triggered after a successful payment.
@login_required
@transaction.atomic
def create_order(request, event_id, quantity):
    event = get_object_or_404(Event, id=event_id)
    total_price = event.price * quantity

    if event.capacity < quantity:
        messages.error(request, f'Sorry, only {event.capacity} tickets left for this event.')
        # Redirect to event detail page or somewhere else
        return redirect('events:event_detail', event_id=event.id) # Assuming this URL exists

    order = Order.objects.create(
        user=request.user,
        total_amount=total_price,
        is_paid=True # Assuming payment is successful
    )

    tickets = []
    for _ in range(quantity):
        ticket = Ticket.objects.create(
            order=order,
            event=event,
            user=request.user
        )
        tickets.append(ticket)
    
    event.capacity -= quantity
    event.save()

    messages.success(request, 'Your order was successful! Your tickets have been generated.')
    return redirect('orders:my_orders')