from django.urls import path

from . import views


app_name = "cargadores"


urlpatterns = [

    path(
        "",
        views.buscar_cargadores,
        name="buscar_cargadores"
    ),

]