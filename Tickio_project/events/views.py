from django.shortcuts import render
from django.views.generic import TemplateView

class HomeView(TemplateView):
    template_name = 'events/home.html'

class EventListView(TemplateView):
    template_name = 'events/event_list.html'  # Crearemos este template después