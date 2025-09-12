from django.urls import path
from . import views

app_name = 'dashboard'

urlpatterns = [
    path('organizer/', views.organizer_dashboard, name='organizer_dashboard'),
]
