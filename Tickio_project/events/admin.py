from django.contrib import admin
from events.models import CategoriaEvento, Evento

@admin.register(CategoriaEvento)
class CategoriaEventoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'descripcion')
    search_fields = ('nombre',)

@admin.register(Evento)
class EventoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'categoria', 'fecha', 'lugar', "organizador", 'cupos_disponibles', 'precio')
    list_filter = ('categoria', 'fecha')
    search_fields = ('nombre', 'lugar')
    date_hierarchy = 'fecha'