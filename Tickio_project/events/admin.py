from django.contrib import admin
from events.models import CategoriaEvento, Evento, TicketType

@admin.register(CategoriaEvento)
class CategoriaEventoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'descripcion')
    search_fields = ('nombre',)

class TicketTypeInline(admin.TabularInline):
    model = TicketType
    extra = 1
    fields = ("name", "price", "capacity", "sold", "active")
    readonly_fields = ("sold",)

@admin.register(Evento)
class EventoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'categoria', 'fecha', 'lugar', "organizador", 'cupos_disponibles', 'precio')
    list_filter = ('categoria', 'fecha')
    search_fields = ('nombre', 'lugar')
    date_hierarchy = 'fecha'
    inlines = [TicketTypeInline]

@admin.register(TicketType)
class TicketTypeAdmin(admin.ModelAdmin):
    list_display = ("name", "event", "price", "capacity", "sold", "active")
    list_filter = ("event", "active")