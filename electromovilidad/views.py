import requests

from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from mapa.views import (obtener_coordenadas, obtener_ruta_osrm,)

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

#*************************************************************
# ***************** FUNCION CALCULAR VIAJE ********************
#**************************************************************
@login_required
def calcular_viaje(request):

    vehiculos = (
        VehiculoElectrico.objects
        .all()
        .order_by(
            "marca",
            "modelo",
            "version"
        )
    )

    resultado = None
    error = None


    if request.method == "POST":

        vehiculo_id = request.POST.get(
            "vehiculo_id"
        )

        origen = request.POST.get(
            "origen",
            ""
        ).strip()

        destino = request.POST.get(
            "destino",
            ""
        ).strip()


        # =========================================
        # VALIDAR DATOS
        # =========================================

        if (
            not vehiculo_id
            or not origen
            or not destino
        ):

            error = (
                "Debes seleccionar un vehículo "
                "e ingresar origen y destino."
            )

        else:

            try:

                vehiculo = (
                    VehiculoElectrico.objects.get(
                        id=vehiculo_id
                    )
                )

            except VehiculoElectrico.DoesNotExist:

                vehiculo = None

                error = (
                    "El vehículo seleccionado "
                    "no es válido."
                )


            if vehiculo:

                # =========================================
                # OBTENER COORDENADAS
                # =========================================

                coordenadas_origen = (
                    obtener_coordenadas(
                        f"{origen}, Chile"
                    )
                )

                coordenadas_destino = (
                    obtener_coordenadas(
                        f"{destino}, Chile"
                    )
                )


                if (
                    not coordenadas_origen
                    or not coordenadas_destino
                ):

                    error = (
                        "No fue posible encontrar "
                        "una de las direcciones."
                    )

                else:

                    # =========================================
                    # RUTA EN AUTO CON OSRM
                    # =========================================

                    ruta = obtener_ruta_osrm(
                        coordenadas_origen,
                        coordenadas_destino,
                        "auto"
                    )


                    if not ruta:

                        error = (
                            "No fue posible calcular "
                            "la ruta."
                        )

                    else:

                        distancia_km = float(
                            ruta["distancia_km"]
                        )

                        autonomia_km = float(
                            vehiculo.autonomia_km
                        )


                        # =========================================
                        # DISTANCIA IDA Y VUELTA
                        # =========================================

                        distancia_ida_vuelta = (
                            distancia_km * 2
                        )


                        # =========================================
                        # VIAJES IDA Y VUELTA
                        # =========================================

                        if distancia_ida_vuelta > 0:

                            viajes_ida_vuelta = int(
                                autonomia_km
                                //
                                distancia_ida_vuelta
                            )

                        else:

                            viajes_ida_vuelta = 0


                        # =========================================
                        # BATERÍA ESTIMADA
                        # =========================================

                        bateria_usada_ida = (
                            distancia_km
                            /
                            autonomia_km
                        ) * 100


                        bateria_usada_ida_vuelta = (
                            distancia_ida_vuelta
                            /
                            autonomia_km
                        ) * 100


                        # =========================================
                        # VALIDAR AUTONOMÍA
                        # =========================================

                        puede_completar_ida = (
                            autonomia_km
                            >=
                            distancia_km
                        )


                        puede_completar_ida_vuelta = (
                            autonomia_km
                            >=
                            distancia_ida_vuelta
                        )


                        distancia_faltante = max(
                            distancia_km
                            -
                            autonomia_km,
                            0
                        )


                        autonomia_restante = max(
                            autonomia_km
                            -
                            distancia_km,
                            0
                        )


                        # =========================================
                        # RESULTADO
                        # =========================================

                        resultado = {

                            "vehiculo":
                                vehiculo,

                            "origen":
                                origen,

                            "destino":
                                destino,

                            "distancia_km":
                                round(
                                    distancia_km,
                                    2
                                ),

                            "distancia_ida_vuelta":
                                round(
                                    distancia_ida_vuelta,
                                    2
                                ),

                            "viajes_ida_vuelta":
                                viajes_ida_vuelta,

                            "bateria_usada_ida":
                                round(
                                    bateria_usada_ida,
                                    2
                                ),

                            "bateria_usada_ida_vuelta":
                                round(
                                    bateria_usada_ida_vuelta,
                                    2
                                ),

                            "puede_completar_ida":
                                puede_completar_ida,

                            "puede_completar_ida_vuelta":
                                puede_completar_ida_vuelta,

                            "distancia_faltante":
                                round(
                                    distancia_faltante,
                                    2
                                ),

                            "autonomia_restante":
                                round(
                                    autonomia_restante,
                                    2
                                ),

                            "origen_lat":
                                coordenadas_origen[
                                    "lat"
                                ],

                            "origen_lon":
                                coordenadas_origen[
                                    "lon"
                                ],

                            "destino_lat":
                                coordenadas_destino[
                                    "lat"
                                ],

                            "destino_lon":
                                coordenadas_destino[
                                    "lon"
                                ],

                            "duracion":
                                ruta[
                                    "duracion_texto"
                                ],
                        }


    return render(
        request,
        "electromovilidad/calcular_viaje.html",
        {
            "vehiculos":
                vehiculos,

            "resultado":
                resultado,

            "error":
                error,
        }
    )