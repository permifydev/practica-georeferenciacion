#!/usr/bin/env bash

set -o errexit

pip install -r requirements.txt

python - <<'PY'
import os
import zipfile

zip_path = "mapa/data/Cartografía_censo2024_R13.gdb.zip"
destino = "mapa/data"

carpeta_gdb = "mapa/data/Cartografía_censo2024_R13.gdb"

if not os.path.exists(carpeta_gdb):
    print("Descomprimiendo cartografía...")
    with zipfile.ZipFile(zip_path, "r") as zip_ref:
        zip_ref.extractall(destino)
    print("Cartografía descomprimida correctamente.")
else:
    print("La cartografía ya existe.")
PY

python manage.py collectstatic --noinput
python manage.py migrate
python manage.py createsuperuser --noinput || true