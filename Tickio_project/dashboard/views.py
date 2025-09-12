from django.shortcuts import render
from django.contrib.auth.decorators import login_required, user_passes_test
from events.models import Event
from orders.models import Ticket
from django.db.models import Sum, Count

def is_organizer(user):
    return user.is_staff

@login_required
@user_passes_test(is_organizer)
def organizer_dashboard(request):
    organizer = request.user
    events = Event.objects.filter(organizer=organizer)
    
    total_sold = 0
    total_tickets_sold = 0
    total_capacity = 0

    for event in events:
        tickets_sold_for_event = Ticket.objects.filter(event=event).count()
        total_sold += tickets_sold_for_event * event.price
        total_tickets_sold += tickets_sold_for_event
        total_capacity += event.capacity

    occupation_percentage = (total_tickets_sold / total_capacity * 100) if total_capacity > 0 else 0

    context = {
        'total_sold': total_sold,
        'total_tickets_sold': total_tickets_sold,
        'occupation_percentage': round(occupation_percentage, 2),
        'events': events
    }
    return render(request, 'dashboard/organizer_dashboard.html', context)