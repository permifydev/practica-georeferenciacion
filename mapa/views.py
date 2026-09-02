import requests
import json

from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from .spatial import buscar_manzana
from django.conf import settings

@login_required
def consulta_view(request):
   

    resultado = None

    

    if request.method == "POST":
        direccion = request.POST.get("direccion")

        print("DIRECCION RECIBIDA:", direccion)

        url = "https://nominatim.openstreetmap.org/search"

        params = {
            "q": direccion,
            "format": "json",
            "limit": 1,
            "addressdetails": 1,
        }

        headers = {
            "User-Agent": "mapa_chile_app/1.0"
        }

        response = requests.get(
            url,
            params=params,
            headers=headers,
            timeout=10
        )

        datos = response.json()

        print("RESPUESTA NOMINATIM:", datos)

        if datos:

            lat = datos[0]["lat"]
            lon = datos[0]["lon"]

            codigo_postal = datos[0].get(
                "address", {}
                ).get(
                    "postcode",
                    "No disponible"
                )

            manzana = buscar_manzana(lat, lon)
            
            resultado = {
                "direccion": datos[0]["display_name"],
                "lat": lat,
                "lon": lon,
                "codigo_postal": codigo_postal,
                "manzana": manzana,
                "manzana_json": json.dumps(manzana["feature"]) if manzana else None,
            }

    return render(
        request,
        "mapa/consulta.html",
        {
            "resultado": resultado
        }
    )
@login_required
def ruta_view(request):

    resultado = None
    error = None

    if request.method == "POST":

        origen = request.POST.get("origen")
        destino = request.POST.get("destino")

        url = "https://maps.googleapis.com/maps/api/distancematrix/json"

        modos = {
            "auto": "driving",
            "caminando": "walking",
            "bicicleta": "bicycling",
        }

        tiempos = {}
        distancia = None
        origen_google = None
        destino_google = None

        for nombre, modo in modos.items():

            params = {
                "origins": origen,
                "destinations": destino,
                "mode": modo,
                "language": "es",
                "key": settings.GOOGLE_MAPS_API_KEY,
            }

            response = requests.get(
                url,
                params=params,
                timeout=10
            )

            datos = response.json()

            print(f"RESPUESTA GOOGLE {nombre}:", datos)

            if datos.get("status") == "OK":

                elemento = datos["rows"][0]["elements"][0]

                if elemento.get("status") == "OK":

                    tiempos[nombre] = elemento["duration"]["text"]

                    if distancia is None:
                        distancia = elemento["distance"]["text"]

                    if origen_google is None:
                        origen_google = datos["origin_addresses"][0]

                    if destino_google is None:
                        destino_google = datos["destination_addresses"][0]

                else:
                    tiempos[nombre] = "No disponible"

            else:
                tiempos[nombre] = "No disponible"

        if origen_google and destino_google:

            resultado = {
                "origen": origen_google,
                "destino": destino_google,
                "distancia": distancia,
                "auto": tiempos.get("auto"),
                "caminando": tiempos.get("caminando"),
                "bicicleta": tiempos.get("bicicleta"),
            }

        else:
            error = "No fue posible calcular la ruta."

    return render(
        request,
        "mapa/ruta.html",
        {
            "resultado": resultado,
            "error": error,
        }
    )  