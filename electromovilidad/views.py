from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from .models import VehiculoElectrico


@login_required
def vehiculos_electricos(request):

    vehiculos = VehiculoElectrico.objects.all().order_by(
        "marca",
        "modelo",
        "version"
    )

    return render(
        request,
        "electromovilidad/vehiculos_electricos.html",
        {
            "vehiculos": vehiculos
        }
    )