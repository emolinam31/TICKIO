from django.urls import path
from .views import HomeView, EventListView, EventDetailView

app_name = "events"

urlpatterns = [
    path("", HomeView.as_view(), name="home"),            # Home tipo e-commerce
    path("events/", EventListView.as_view(), name="list"),# Explorador/listado
    path("events/<slug:slug>/", EventDetailView.as_view(), name="detail"),
]
