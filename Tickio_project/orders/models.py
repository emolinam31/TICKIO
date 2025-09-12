from django.db import models
from django.contrib.auth.models import User
from events.models import Event
import uuid
import qrcode
from io import BytesIO
from django.core.files import File

class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    is_paid = models.BooleanField(default=False)

    def __str__(self):
        return f"Order {self.id} by {self.user.username}"

class Ticket(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='tickets')
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    ticket_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    qr_code = models.ImageField(upload_to='qr_codes/', blank=True)

    def __str__(self):
        return f"Ticket {self.ticket_id} for {self.event.name}"

    def save(self, *args, **kwargs):
        if not self.qr_code:
            qr_image = qrcode.make(str(self.ticket_id))
            canvas = qr_image.get_image()
            fname = f'qr_code-{self.ticket_id}.png'
            buffer = BytesIO()
            canvas.save(buffer, 'PNG')
            self.qr_code.save(fname, File(buffer), save=False)
        super().save(*args, **kwargs)