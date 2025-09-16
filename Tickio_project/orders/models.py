from django.db import models
from django.conf import settings
from django.utils import timezone
from events.models import Evento, TicketType
import uuid


class Order(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, null=True, blank=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=20, default='created')
    total_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0)

    def __str__(self):
        return f"Order #{self.id}"


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    event = models.ForeignKey(Evento, on_delete=models.PROTECT)
    ticket_type = models.ForeignKey(TicketType, on_delete=models.PROTECT)
    name = models.CharField(max_length=120)
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField()
    line_total = models.DecimalField(max_digits=12, decimal_places=2)

    def __str__(self):
        return f"{self.quantity} x {self.name}"


class Ticket(models.Model):
    order = models.ForeignKey(Order, on_delete=models.PROTECT, related_name='tickets')
    ticket_type = models.ForeignKey(TicketType, on_delete=models.PROTECT)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT)
    event = models.ForeignKey(Evento, on_delete=models.PROTECT)
    unique_code = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    is_used = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Ticket for {self.event.nombre} - {self.ticket_type.name}'

