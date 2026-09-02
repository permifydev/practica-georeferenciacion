from django.urls import path
from . import views

app_name = "mapa"

urlpatterns = [
    path("consulta/", views.consulta_view, name="consulta"),
    path("ruta/", views.ruta_view, name="ruta"),
]