from django.utils import timezone
from django.views.generic import TemplateView
from django.db.models import Sum
from django.db.models.functions import Coalesce

from .models import Event, Category, Venue

class HomeView(TemplateView):
    template_name = "events/home.html"

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)

        # Catálogo para filtros rápidos
        ctx["categories"] = Category.objects.order_by("name")
        ctx["cities"] = Venue.objects.values_list("city", flat=True).distinct().order_by("city")

        base_qs = Event.objects.filter(is_published=True)

        # Destacados: si tienes `is_featured`, úsalo; si no, cae a "tendencias"
        featured = base_qs.filter(is_featured=True)[:8] if hasattr(Event, "is_featured") else Event.objects.none()
        if not featured.exists():
            featured = base_qs.annotate(
                sold_total=Coalesce(Sum("ticket_types__sold"), 0)
            ).order_by("-sold_total")[:8]

        # Tendencias por vendidos
        trending = base_qs.annotate(
            sold_total=Coalesce(Sum("ticket_types__sold"), 0)
        ).order_by("-sold_total")[:8]

        # Próximos por fecha
        upcoming = base_qs.filter(date_start__gte=timezone.now()).order_by("date_start")[:8]

        ctx.update({
            "featured_events": featured,
            "trending_events": trending,
            "upcoming_events": upcoming,
        })
        return ctx
