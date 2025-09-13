from django.shortcuts import render
from django.views.generic import TemplateView, ListView, DetailView
from .models import Evento, CategoriaEvento

class HomeView(TemplateView):
    template_name = 'events/home.html'

class EventListView(ListView):
    model = Evento
    template_name = 'events/list_events.html'
    context_object_name = 'eventos'
    ordering = ['-fecha']
    paginate_by = 12

    def get_queryset(self):
        queryset = super().get_queryset()
        
        # Get filter parameters from URL
        nombre = self.request.GET.get("nombre")
        categoria = self.request.GET.get("categoria")
        lugar = self.request.GET.get("lugar")
        fecha = self.request.GET.get("fecha")
        
        if nombre:
            queryset = queryset.filter(nombre__icontains=nombre)
        if categoria:
            queryset = queryset.filter(categoria__nombre=categoria)
        if lugar:
            queryset = queryset.filter(lugar__icontains=lugar)
        if fecha:
            queryset = queryset.filter(fecha=fecha)

        return queryset


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categorias'] = CategoriaEvento.objects.all()
        context['lugares'] = Evento.objects.values_list('lugar', flat=True).distinct()

        # Calcular el total de cupos disponibles por evento
        eventos = context['eventos']
        total_disponibles_dict = {}
        for evento in eventos:
            total = sum([tt.remaining for tt in evento.ticket_types.all()])
            total_disponibles_dict[evento.id] = total
        context['total_disponibles_dict'] = total_disponibles_dict
        return context
    
class EventDetailView(DetailView):
    model = Evento
    template_name = "events/detail_events.html"
    context_object_name = "evento"
