from django.urls import path
from . import views

app_name = 'events'

urlpatterns = [
    path("", views.HomeView.as_view(), name="home"),
    path("events/", views.EventListView.as_view(), name="events"),
    path("events/<int:pk>/", views.EventDetailView.as_view(), name="event_detail"),
    
    # URLs del organizador
    path("mis-eventos/", views.mis_eventos, name="mis_eventos"),
    path("evento/crear/", views.crear_evento, name="crear_evento"),
    path("evento/<int:pk>/editar/", views.editar_evento, name="editar_evento"),
    path("evento/<int:pk>/estado/", views.cambiar_estado_evento, name="cambiar_estado_evento"),
]