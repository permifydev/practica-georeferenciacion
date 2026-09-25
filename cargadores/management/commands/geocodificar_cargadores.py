import time

from django.core.management.base import BaseCommand

from cargadores.models import CargadorElectrico
from mapa.views import obtener_coordenadas


class Command(BaseCommand):

    help = "Obtiene y guarda coordenadas de cargadores eléctricos"

    def handle(self, *args, **options):

        cargadores = CargadorElectrico.objects.filter(
            latitud__isnull=True,
            longitud__isnull=True
        )

        total = cargadores.count()

        self.stdout.write(
            f"Cargadores pendientes: {total}"
        )

        actualizados = 0
        sin_resultado = 0

        for numero, cargador in enumerate(
            cargadores,
            start=1
        ):

            if not cargador.direccion:

                sin_resultado += 1
                continue

            partes_direccion = [
                cargador.direccion,
                cargador.comuna,
                cargador.region,
                "Chile"
            ]

            direccion_busqueda = ", ".join(
                parte
                for parte in partes_direccion
                if parte
            )

            self.stdout.write(
                f"{numero}/{total} - "
                f"{direccion_busqueda}"
            )

            try:

                coordenadas = obtener_coordenadas(
                    direccion_busqueda
                )

                if coordenadas:

                    cargador.latitud = (
                        coordenadas["lat"]
                    )

                    cargador.longitud = (
                        coordenadas["lon"]
                    )

                    cargador.save(
                        update_fields=[
                            "latitud",
                            "longitud"
                        ]
                    )

                    actualizados += 1

                    self.stdout.write(
                        self.style.SUCCESS(
                            "Coordenadas encontradas"
                        )
                    )

                else:

                    sin_resultado += 1

                    self.stdout.write(
                        self.style.WARNING(
                            "No se encontraron coordenadas"
                        )
                    )

            except Exception as error:

                sin_resultado += 1

                self.stdout.write(
                    self.style.ERROR(
                        f"Error: {error}"
                    )
                )

            time.sleep(1)


        self.stdout.write(
            self.style.SUCCESS(
                f"Actualizados: {actualizados}"
            )
        )

        self.stdout.write(
            self.style.WARNING(
                f"Sin coordenadas: {sin_resultado}"
            )
        )