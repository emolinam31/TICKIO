from django.db import models

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