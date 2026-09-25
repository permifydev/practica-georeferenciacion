import math

from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from mapa.views import obtener_coordenadas

from .models import CargadorElectrico


def calcular_distancia(
    latitud_origen,
    longitud_origen,
    latitud_destino,
    longitud_destino
):

    radio_tierra = 6371

    latitud_origen = math.radians(
        latitud_origen
    )

    longitud_origen = math.radians(
        longitud_origen
    )

    latitud_destino = math.radians(
        latitud_destino
    )

    longitud_destino = math.radians(
        longitud_destino
    )

    diferencia_latitud = (
        latitud_destino
        - latitud_origen
    )

    diferencia_longitud = (
        longitud_destino
        - longitud_origen
    )

    a = (
        math.sin(
            diferencia_latitud / 2
        ) ** 2
        +
        math.cos(
            latitud_origen
        )
        *
        math.cos(
            latitud_destino
        )
        *
        math.sin(
            diferencia_longitud / 2
        ) ** 2
    )

    c = 2 * math.atan2(
        math.sqrt(a),
        math.sqrt(1 - a)
    )

    return radio_tierra * c


def obtener_cargadores_cercanos(
    latitud_usuario,
    longitud_usuario
):

    cargadores = (
        CargadorElectrico.objects
        .filter(
            latitud__isnull=False,
            longitud__isnull=False
        )
    )

    resultados = []


    for cargador in cargadores:

        distancia = calcular_distancia(
            latitud_usuario,
            longitud_usuario,
            float(
                cargador.latitud
            ),
            float(
                cargador.longitud
            )
        )


        resultados.append(
            {
                "cargador":
                    cargador,
                "distancia":
                    round(
                        distancia,
                        2
                    )
            }
        )


    return sorted(
        resultados,
        key=lambda resultado:
            resultado["distancia"]
    )[:3]


@login_required
def buscar_cargadores(request):

    cargadores_cercanos = []

    direccion = ""

    coordenadas_usuario = None

    error = None


    if request.method == "POST":

        direccion = request.POST.get(
            "direccion",
            ""
        ).strip()

        latitud = request.POST.get(
            "latitud",
            ""
        ).strip()

        longitud = request.POST.get(
            "longitud",
            ""
        ).strip()


        # =========================================
        # BÚSQUEDA POR UBICACIÓN ACTUAL
        # =========================================

        if latitud and longitud:

            try:

                latitud_usuario = float(
                    latitud
                )

                longitud_usuario = float(
                    longitud
                )

                coordenadas_usuario = {
                    "lat":
                        latitud_usuario,
                    "lon":
                        longitud_usuario
                }

                direccion = (
                    "Mi ubicación actual"
                )


                cargadores_cercanos = (
                    obtener_cargadores_cercanos(
                        latitud_usuario,
                        longitud_usuario
                    )
                )


            except ValueError:

                error = (
                    "Las coordenadas recibidas "
                    "no son válidas."
                )


        # =========================================
        # BÚSQUEDA POR DIRECCIÓN
        # =========================================

        elif direccion:

            coordenadas_usuario = (
                obtener_coordenadas(
                    f"{direccion}, Chile"
                )
            )


            if not coordenadas_usuario:

                error = (
                    "No se pudo encontrar "
                    "la dirección ingresada."
                )

            else:

                latitud_usuario = float(
                    coordenadas_usuario["lat"]
                )

                longitud_usuario = float(
                    coordenadas_usuario["lon"]
                )


                cargadores_cercanos = (
                    obtener_cargadores_cercanos(
                        latitud_usuario,
                        longitud_usuario
                    )
                )


        else:

            error = (
                "Debes ingresar una dirección "
                "o usar tu ubicación actual."
            )


    return render(
        request,
        "cargadores/buscar_cargadores.html",
        {
            "direccion":
                direccion,
            "cargadores_cercanos":
                cargadores_cercanos,
            "coordenadas_usuario":
                coordenadas_usuario,
            "error":
                error,
        }
    )