from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.generic import TemplateView, ListView, DetailView
from django.core.exceptions import PermissionDenied
from .models import Evento, CategoriaEvento
from .forms import EventoForm, TicketTypeFormSet
from .decorators import organizador_required

class HomeView(TemplateView):
    def get_template_names(self):
        if self.request.user.is_authenticated and self.request.user.tipo == 'organizador':
            return ['events/organizador_home.html']
        return ['events/home.html']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.is_authenticated and self.request.user.tipo == 'organizador':
            context['eventos'] = Evento.objects.filter(organizador=self.request.user).order_by('-fecha_creacion')[:6]
        return context

class EventListView(ListView):
    model = Evento
    template_name = 'events/list_events.html'
    context_object_name = 'eventos'
    ordering = ['-fecha']
    paginate_by = 12

    def get_queryset(self):
        queryset = super().get_queryset()
        # Solo mostrar eventos publicados para el público general
        if not self.request.user.is_authenticated or self.request.user.tipo != 'organizador':
            queryset = queryset.filter(estado='publicado')
        
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
        return context


class EventDetailView(DetailView):
    model = Evento
    template_name = 'events/detail_events.html'
    context_object_name = 'evento'

    def get_queryset(self):
        qs = super().get_queryset().select_related('categoria', 'organizador').prefetch_related('ticket_types')
        # Solo permitir ver eventos publicados a no organizadores
        if not self.request.user.is_authenticated or self.request.user.tipo != 'organizador':
            qs = qs.filter(estado='publicado')
        return qs

@login_required
@organizador_required
def mis_eventos(request):
    eventos = Evento.objects.filter(organizador=request.user).order_by('-fecha_creacion')
    return render(request, 'events/mis_eventos.html', {'eventos': eventos})

@login_required
@organizador_required
def crear_evento(request):
    if request.method == 'POST':
        form = EventoForm(request.POST, organizador=request.user)
        if form.is_valid():
            evento = form.save()
            formset = TicketTypeFormSet(request.POST, instance=evento)
            if formset.is_valid():
                formset.save()
                messages.success(request, 'Evento creado exitosamente.')
                return redirect('events:mis_eventos')
            else:
                # Si formset falla, no perder evento: mostrar errores
                messages.error(request, 'Corrige los errores en los tipos de boleto.')
    else:
        form = EventoForm(organizador=request.user)
    formset = TicketTypeFormSet(request.POST or None)
    return render(request, 'events/evento_form.html', {
        'form': form,
        'formset': formset,
        'action': 'Crear',
        'titulo': 'Crear Nuevo Evento'
    })

@login_required
@organizador_required
def editar_evento(request, pk):
    evento = get_object_or_404(Evento, pk=pk, organizador=request.user)
    if request.method == 'POST':
        form = EventoForm(request.POST, instance=evento)
        formset = TicketTypeFormSet(request.POST, instance=evento)
        if form.is_valid() and formset.is_valid():
            form.save()
            formset.save()
            messages.success(request, 'Evento actualizado exitosamente.')
            return redirect('events:mis_eventos')
    else:
        form = EventoForm(instance=evento)
        formset = TicketTypeFormSet(instance=evento)
    return render(request, 'events/evento_form.html', {
        'form': form,
        'formset': formset,
        'action': 'Editar',
        'titulo': 'Editar Evento'
    })

@login_required
@organizador_required
def cambiar_estado_evento(request, pk):
    evento = get_object_or_404(Evento, pk=pk, organizador=request.user)
    nuevo_estado = request.POST.get('estado')
    if nuevo_estado in ['borrador', 'publicado', 'pausado']:
        evento.estado = nuevo_estado
        evento.save()
        messages.success(request, f'Estado del evento actualizado a {nuevo_estado}.')
    else:
        messages.error(request, 'Estado no válido.')
    return redirect('events:mis_eventos')
