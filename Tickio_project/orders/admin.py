from django.contrib import admin
from .models import Order, Ticket

class TicketInline(admin.TabularInline):
    model = Ticket
    extra = 0
    readonly_fields = ('ticket_id', 'qr_code')

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'created_at', 'total_amount', 'is_paid')
    list_filter = ('is_paid', 'created_at')
    search_fields = ('user__username', 'id')
    inlines = [TicketInline]

@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):
    list_display = ('ticket_id', 'event', 'user', 'order')
    list_filter = ('event',)
    search_fields = ('user__username', 'event__name', 'ticket_id')