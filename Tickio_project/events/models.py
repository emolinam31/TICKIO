from django.db import models

class CategoriaEvento(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField()

    class Meta:
        verbose_name = "Categoría de Evento"
        verbose_name_plural = "Categorías de Eventos"

    def __str__(self):
        return self.nombre

class Evento(models.Model):
    ESTADO_CHOICES = [
        ('borrador', 'Borrador'),
        ('publicado', 'Publicado'),
        ('pausado', 'Pausado'),
    ]
    
    nombre = models.CharField(max_length=200)
    descripcion = models.TextField(blank=True)
    categoria = models.ForeignKey(
        CategoriaEvento, 
        on_delete=models.PROTECT,
        related_name='eventos'
    )
    fecha = models.DateField()
    lugar = models.CharField(max_length=200)
    organizador = models.ForeignKey(
        'accounts.CustomUser',
        on_delete=models.CASCADE,
        related_name='eventos_organizados',
        limit_choices_to={'tipo': 'organizador'},
        null=True,  # Permitir valores nulos temporalmente para el script de población
        blank=True
    )
    cupos_disponibles = models.PositiveIntegerField()
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    estado = models.CharField(
        max_length=20,
        choices=ESTADO_CHOICES,
        default='borrador'
    )
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Evento"
        verbose_name_plural = "Eventos"
        ordering = ['-fecha', 'nombre']

    def __str__(self):
        return f"{self.nombre} - {self.fecha}"

    def esta_agotado(self):
        return self.cupos_disponibles <= 0

    @property
    def has_ticket_types(self):
        return self.ticket_types.exists()

    def total_available(self):
        if not self.has_ticket_types:
            return self.cupos_disponibles
        return sum(tt.available for tt in self.ticket_types.filter(active=True))

    def min_ticket_price(self):
        if not self.has_ticket_types:
            return self.precio
        prices = list(self.ticket_types.filter(active=True).values_list('price', flat=True))
        return min(prices) if prices else self.precio

    def get_available_ticket_types(self):
        if not self.has_ticket_types:
            return []
        return self.ticket_types.filter(active=True, capacity__gt=models.F('sold')).order_by('price')

    def get_ticket_by_name(self, name: str):
        if not self.has_ticket_types:
            return None
        return (
            self.ticket_types.filter(name__iexact=name, active=True)
            .order_by('price')
            .first()
        )

    def general_ticket(self):
        return self.get_ticket_by_name('General')

    def vip_ticket(self):
        return self.get_ticket_by_name('VIP')


class TicketType(models.Model):
    event = models.ForeignKey(
        Evento,
        on_delete=models.CASCADE,
        related_name='ticket_types'
    )
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    capacity = models.PositiveIntegerField()
    sold = models.PositiveIntegerField(default=0)
    active = models.BooleanField(default=True)

    class Meta:
        verbose_name = 'Tipo de Boleto'
        verbose_name_plural = 'Tipos de Boleto'
        constraints = [
            models.CheckConstraint(check=models.Q(sold__gte=0), name='tickettype_sold_gte_0'),
            models.CheckConstraint(check=models.Q(capacity__gte=0), name='tickettype_capacity_gte_0'),
            models.CheckConstraint(check=models.Q(price__gte=0), name='tickettype_price_gte_0'),
        ]

    def __str__(self):
        return f"{self.name} ({self.event.nombre})"

    @property
    def available(self):
        return max(self.capacity - self.sold, 0)