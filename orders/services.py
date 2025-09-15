from decimal import Decimal
from typing import Dict, Tuple
from django.db import transaction
from django.db.models import F
from .models import Order, OrderItem
from events.models import TicketType

class PaymentGateway:
    def charge(self, amount: Decimal, metadata: dict | None = None) -> Tuple[bool, str]:
        raise NotImplementedError

def checkout(cart: Dict[str, dict], user=None, gateway: PaymentGateway | None = None) -> Order:
    if not cart:
        raise ValueError("El carrito está vacío")

    from payments.adapters.dummy import DummyGateway
    gateway = gateway or DummyGateway()

    with transaction.atomic():
        order = Order.objects.create(user=user)
        total = Decimal('0.00')

        for key, data in cart.items():
            ticket_type = (
                TicketType.objects.select_for_update()
                .select_related('event')
                .get(pk=data['ticket_type_id'], active=True)
            )
            quantity = int(data['quantity'])

            if ticket_type.sold + quantity > ticket_type.capacity:
                raise ValueError(f"No hay disponibilidad suficiente para {ticket_type.name}")

            TicketType.objects.filter(pk=ticket_type.pk).update(sold=F('sold') + quantity)

            line_total = ticket_type.price * quantity
            total += line_total

            OrderItem.objects.create(
                order=order,
                event=ticket_type.event,
                ticket_type=ticket_type,
                name=ticket_type.name,
                unit_price=ticket_type.price,
                quantity=quantity,
                line_total=line_total,
            )

        ok, reference = gateway.charge(total, metadata={"order_id": order.id})
        if not ok:
            raise ValueError("Pago rechazado")

        order.total_amount = total
        order.status = 'paid'
        order.save()

    return order


