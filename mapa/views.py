import requests
import json

from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from .spatial import buscar_manzana


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