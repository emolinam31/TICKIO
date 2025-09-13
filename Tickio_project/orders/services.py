from django.db import transaction
from django.db.models import F
from events.models import TicketType
from .models import Order, OrderItem
from payments.adapters.dummy import DummyPaymentGateway


class NotEnoughTickets(Exception):
    """Se lanza cuando no hay suficientes tickets disponibles."""
    pass


def checkout(cart, gateway=None):
    if gateway is None:
        gateway = DummyPaymentGateway()

    with transaction.atomic():
        order = Order.objects.create(total=0)
        total = 0

        for ticket_id, item in cart.items():
            ticket = (
                TicketType.objects
                .select_for_update()  # bloquea la fila hasta fin de la transacción
                .get(id=ticket_id)
            )

            quantity = item["quantity"]

            if ticket.capacity - ticket.sold < quantity:
                raise NotEnoughTickets(f"No hay suficientes entradas para {ticket.name}")

            # Actualizar las entradas vendidas con F()
            ticket.sold = F("sold") + quantity
            ticket.save()

            subtotal = ticket.price * quantity
            total += subtotal

            OrderItem.objects.create(
                order=order,
                ticket_type=ticket,
                quantity=quantity,
                price=ticket.price,
            )

        order.total = total

        # Procesar pago
        success = gateway.charge(total)
        if success:
            order.status = "paid"
        else:
            order.status = "failed"

        order.save()

    return order
