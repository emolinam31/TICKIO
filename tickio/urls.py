from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("events.urls")),
    path("accounts/", include("accounts.urls", namespace="accounts")),
    path("orders/", include("orders.urls")),
    path("about/", TemplateView.as_view(template_name="about.html"), name="about"),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
