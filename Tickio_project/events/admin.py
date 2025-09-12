from django.contrib import admin
from .models import Event, TicketType

class TicketTypeInline(admin.TabularInline):
    model = TicketType
    extra = 1   # cuántas filas vacías mostrar por defecto
    fields = ("name", "price", "capacity", "sold", "active")
    readonly_fields = ("sold",)

@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ("title", "slug", "start", "end")
    prepopulated_fields = {"slug": ("title",)}
    inlines = [TicketTypeInline]

@admin.register(TicketType)
class TicketTypeAdmin(admin.ModelAdmin):
    list_display = ("name", "event", "price", "capacity", "sold", "active")
    list_filter = ("event", "active")
