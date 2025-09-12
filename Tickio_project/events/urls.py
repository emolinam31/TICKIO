from django.urls import path
from . import views

urlpatterns = [
    path("", views.HomeView.as_view(), name = "home"),
    path("events/", views.EventListView.as_view(), name = "events"),
]
