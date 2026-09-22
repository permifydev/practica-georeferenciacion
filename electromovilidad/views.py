import requests

from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from mapa.views import obtener_coordenadas

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

    vehiculos = VehiculoElectrico.objects.all().order_by(
        "marca",
        "modelo",
        "version"
    )

    resultado = None
    error = None

    if request.method == "POST":

        vehiculo_id = request.POST.get(
            "vehiculo_id"
        )

        origen = request.POST.get(
            "origen"
        )

        destino = request.POST.get(
            "destino"
        )

        if not vehiculo_id or not origen or not destino:

            error = "Debes seleccionar un vehículo e ingresar origen y destino."

        else:

            try:

                vehiculo = VehiculoElectrico.objects.get(
                    id=vehiculo_id
                )

            except VehiculoElectrico.DoesNotExist:

                vehiculo = None
                error = "El vehículo seleccionado no existe."


            if vehiculo:

                url = (
                    "https://maps.googleapis.com/maps/api/"
                    "distancematrix/json"
                )

                params = {
                    "origins": origen,
                    "destinations": destino,
                    "mode": "driving",
                    "language": "es",
                    "key": settings.GOOGLE_MAPS_API_KEY,
                }

                response = requests.get(
                    url,
                    params=params,
                    timeout=10
                )

                datos = response.json()

                if datos.get("status") == "OK":

                    elemento = datos["rows"][0]["elements"][0]

                    if elemento.get("status") == "OK":

                        distancia_texto = elemento["distance"]["text"]

                        distancia_metros = elemento["distance"]["value"]

                        distancia_km = distancia_metros / 1000

                        autonomia_km = float(
                            vehiculo.autonomia_km
                        )

                        distancia_ida_vuelta = (
                            distancia_km * 2
                        )

                        puede_completar_ida = (
                            autonomia_km >= distancia_km
                        )

                        puede_completar_ida_vuelta = (
                            autonomia_km >= distancia_ida_vuelta
                        )

                        distancia_faltante = max(
                            distancia_km - autonomia_km,
                            0
                        )

                        autonomia_restante = max(
                            autonomia_km - distancia_km,
                            0
                        )

                        # CALCULO CUANTAS IDAS *********************************************************************

                        #viajes_solo_ida = int(
                         #   autonomia_km // distancia_km
                        #)

                        viajes_ida_vuelta = int(
                            autonomia_km // distancia_ida_vuelta
                        )

                        bateria_usada_ida = (
                            distancia_km / autonomia_km
                        ) * 100

                        bateria_usada_ida_vuelta = (
                            distancia_ida_vuelta / autonomia_km
                        ) * 100

                        coordenadas_origen = obtener_coordenadas(
                            datos["origin_addresses"][0]
                        )

                        coordenadas_destino = obtener_coordenadas(
                            datos["destination_addresses"][0]
                        )


                        resultado = {
                            "vehiculo": vehiculo,

                            "origen": datos["origin_addresses"][0],

                            "destino": datos["destination_addresses"][0],

                            "distancia_texto": distancia_texto,

                            "distancia_km": round(
                                distancia_km,
                                2
                            ),

                            "puede_completar_ida": puede_completar_ida,

                            "puede_completar_ida_vuelta": (
                                puede_completar_ida_vuelta
                            ),

                            "distancia_faltante": round(
                                distancia_faltante,
                                2
                            ),

                            "autonomia_restante": round(
                                autonomia_restante,
                                2
                            ),

                            "distancia_ida_vuelta": round(
                                distancia_ida_vuelta,
                                2
                            ),
                            #CALCULO DE VIAJES DE IDA *******************************************************
                            #"viajes_solo_ida": viajes_solo_ida,

                            "viajes_ida_vuelta": viajes_ida_vuelta,

                            "bateria_usada_ida": round(
                                bateria_usada_ida,
                                2
                            ),

                            "bateria_usada_ida_vuelta": round(
                                bateria_usada_ida_vuelta,
                                2
                            ),

                            "origen_lat": (
                                coordenadas_origen["lat"]
                                if coordenadas_origen
                                else None
                            ),

                            "origen_lon": (
                                coordenadas_origen["lon"]
                                if coordenadas_origen
                                else None
                            ),

                            "destino_lat": (
                                coordenadas_destino["lat"]
                                if coordenadas_destino
                                else None
                            ),

                            "destino_lon": (
                                coordenadas_destino["lon"]
                                if coordenadas_destino
                                else None
                            ),
                        }

                    else:

                        error = "No fue posible calcular la distancia."

                else:

                    error = "Error al consultar Google Maps."


    return render(
        request,
        "electromovilidad/calcular_viaje.html",
        {
            "vehiculos": vehiculos,
            "resultado": resultado,
            "error": error
        }
    )