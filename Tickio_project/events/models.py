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
    nombre = models.CharField(max_length=200)
    categoria = models.ForeignKey(
        CategoriaEvento, 
        on_delete=models.PROTECT,
        related_name='eventos'
    )
    fecha = models.DateField()
    lugar = models.CharField(max_length=200)
    organizador = models.CharField(max_length=100, default="Sin Organizador")
    cupos_disponibles = models.PositiveIntegerField()
    precio = models.DecimalField(max_digits=10, decimal_places=2)
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

# Modelo TicketType para compatibilidad con la app orders
class TicketType(models.Model):
    event = models.ForeignKey(Evento, related_name='ticket_types', on_delete=models.CASCADE)
    name = models.CharField(max_length=120)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    capacity = models.PositiveIntegerField()
    sold = models.PositiveIntegerField(default=0)
    active = models.BooleanField(default=True)

    class Meta:
        verbose_name = 'Tipo de boleto'
        verbose_name_plural = 'Tipos de boleto'

    def __str__(self):
        return f"{self.name} — {self.event}"

    @property
    def remaining(self):
        return max(self.capacity - self.sold, 0)

    def can_sell(self, quantity=1):
        return (self.sold + quantity) <= self.capacity
