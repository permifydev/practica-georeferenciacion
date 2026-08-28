import json
import os

import geopandas as gpd
from shapely.geometry import Point

# para buscar la manzana censal correspondiente a una coordenada.

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

DATA_DIR = os.path.join(BASE_DIR, "data")

MANZANAS_GDB = os.path.join(
    DATA_DIR,
    "Cartografia_censo2024_Pais.gdb"
)

MANZANAS_LAYER = "Manzanas_CPV24"


def buscar_manzana(lat, lng):

    if lat is None or lng is None:
        return None

    try:
        lat = float(lat)
        lng = float(lng)

        punto = Point(lng, lat)

        # Busca solamente alrededor del punto,
        # no carga todas las manzanas de Chile.
        margen = 0.002

        bbox = (
            lng - margen,
            lat - margen,
            lng + margen,
            lat + margen
        )

        print("Buscando manzanas cercanas a:", lat, lng)

        gdf = gpd.read_file(
            MANZANAS_GDB,
            layer=MANZANAS_LAYER,
            bbox=bbox
        )

        print("Manzanas candidatas:", len(gdf))

        if gdf.empty:
            return None

        # Dejamos las geometrías en latitud/longitud.
        gdf = gdf.to_crs(epsg=4326)

        # Busca la manzana que contiene el punto.
        resultado = gdf[gdf.geometry.covers(punto)]

        if resultado.empty:
            resultado = gdf[
                gdf.geometry.intersects(
                    punto.buffer(0.00005)
                )
            ]

        if resultado.empty:
            print("No se encontró una manzana.")
            return None

        encontrado = resultado.iloc[[0]]

        geojson = json.loads(
            encontrado.to_json()
        )

        feature = geojson["features"][0]

        props = feature["properties"]

        print("PROPIEDADES DE LA MANZANA:")####
        print(props)#########

        print(
            "Manzana encontrada:",
            props.get("COMUNA"),
            props.get("DISTRITO"),
            props.get("COD_MANZANA")
        )

        return {
            "props": props,
            "feature": feature,
        }

    except Exception as e:

        print("Error buscando manzana:", e)

        return None