from django.urls import path
from . import views


app_name = "electromovilidad"


urlpatterns = [

    path(
        "vehiculos/",
        views.vehiculos_electricos,
        name="vehiculos_electricos"
    ),

]