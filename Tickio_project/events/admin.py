from django.contrib import admin
from .models import Event

@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ('name', 'organizer', 'date', 'location', 'capacity', 'price')
    list_filter = ('date', 'location', 'organizer')
    search_fields = ('name', 'description', 'organizer__username')