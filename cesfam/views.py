import json
from pathlib import Path
from math import radians, sin, cos, sqrt, atan2

import requests

from django.contrib.auth.decorators import login_required
from django.shortcuts import render


def calcular_distancia(lat1, lon1, lat2, lon2):

    radio_tierra = 6371

    lat1 = radians(lat1)
    lon1 = radians(lon1)
    lat2 = radians(lat2)
    lon2 = radians(lon2)

    diferencia_lat = lat2 - lat1
    diferencia_lon = lon2 - lon1

    a = (
        sin(diferencia_lat / 2) ** 2
        + cos(lat1)
        * cos(lat2)
        * sin(diferencia_lon / 2) ** 2
    )

    c = 2 * atan2(
        sqrt(a),
        sqrt(1 - a)
    )

    distancia = radio_tierra * c

    return distancia


@login_required
def cesfam_view(request):

    ruta_geojson = (
        Path(__file__).resolve().parent
        / "data"
        / "cesfam_rm.geojson"
    )

    with open(
        ruta_geojson,
        "r",
        encoding="utf-8"
    ) as archivo:
        datos = json.load(archivo)

    direccion = ""
    ubicacion_usuario = None
    error = None
    cesfam_cercanos = []

    if request.method == "POST":

        direccion = request.POST.get(
            "direccion",
            ""
        ).strip()

        latitud_post = request.POST.get(
            "latitud_usuario"
        )

        longitud_post = request.POST.get(
            "longitud_usuario"
        )

        latitud_usuario = None
        longitud_usuario = None

        if latitud_post and longitud_post:

            latitud_usuario = float(
                latitud_post
            )

            longitud_usuario = float(
                longitud_post
            )

            ubicacion_usuario = {
                "latitud": latitud_usuario,
                "longitud": longitud_usuario
            }

        elif direccion:

            url = "https://nominatim.openstreetmap.org/search"

            parametros = {
                "q": direccion,
                "format": "json",
                "limit": 1,
                "countrycodes": "cl"
            }

            headers = {
                "User-Agent": "Addrss-CESFAM/1.0"
            }

            respuesta = requests.get(
                url,
                params=parametros,
                headers=headers,
                timeout=10
            )

            resultados = respuesta.json()

            if resultados:

                latitud_usuario = float(
                    resultados[0]["lat"]
                )

                longitud_usuario = float(
                    resultados[0]["lon"]
                )

                ubicacion_usuario = {
                    "latitud": latitud_usuario,
                    "longitud": longitud_usuario
                }

            else:

                error = "No se encontró la dirección ingresada."

        if (
            latitud_usuario is not None
            and longitud_usuario is not None
        ):

            for establecimiento in datos["features"]:

                propiedades = establecimiento["properties"]

                latitud_cesfam = propiedades.get(
                    "latitud"
                )

                longitud_cesfam = propiedades.get(
                    "longitud"
                )

                if (
                    latitud_cesfam is not None
                    and longitud_cesfam is not None
                ):

                    distancia = calcular_distancia(
                        latitud_usuario,
                        longitud_usuario,
                        float(latitud_cesfam),
                        float(longitud_cesfam)
                    )

                    cesfam_cercanos.append({
                        "nombre": propiedades.get("nombre"),
                        "via": propiedades.get("via"),
                        "direccion": propiedades.get("direccion"),
                        "numero": propiedades.get("numero"),
                        "comuna": propiedades.get("nom_comuna"),
                        "fono": propiedades.get("fono"),
                        "latitud": float(latitud_cesfam),
                        "longitud": float(longitud_cesfam),
                        "distancia": round(distancia, 2)
                    })

            cesfam_cercanos.sort(
                key=lambda cesfam: cesfam["distancia"]
            )

            cesfam_cercanos = cesfam_cercanos[:3]

    return render(
        request,
        "cesfam/cesfam.html",
        {
            "cesfam_geojson": json.dumps(
                datos,
                ensure_ascii=False
            ),
            "direccion": direccion,
            "ubicacion_usuario": ubicacion_usuario,
            "cesfam_cercanos": cesfam_cercanos,
            "cesfam_cercanos_json": json.dumps(
                cesfam_cercanos,
                ensure_ascii=False
            ),
            "error": error
        }
    )
