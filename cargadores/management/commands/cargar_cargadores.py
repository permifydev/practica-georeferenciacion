from pathlib import Path

import openpyxl

from django.core.management.base import BaseCommand

from cargadores.models import CargadorElectrico


class Command(BaseCommand):

    help = "Carga los cargadores eléctricos desde el archivo Excel"

    def handle(self, *args, **options):

        ruta_excel = (
            Path(__file__)
            .resolve()
            .parent
            .parent
            .parent
            / "data"
            / "cargadores_electricos_chile_completo.xlsx"
        )

        if not ruta_excel.exists():

            self.stdout.write(
                self.style.ERROR(
                    f"No se encontró el archivo: {ruta_excel}"
                )
            )

            return


        libro = openpyxl.load_workbook(
            ruta_excel,
            data_only=True
        )


        hoja = libro[
            "Puntos_recarga_Chile"
        ]


        cargados = 0
        existentes = 0


        for fila in hoja.iter_rows(
            min_row=2,
            values_only=True
        ):

            (
                id_excel,
                region,
                provincia,
                comuna,
                tipo_ubicacion,
                nombre,
                direccion,
                conectores_publicados,
                tipo_conector,
                potencia_kw,
                latitud,
                longitud,
                fuente_nombre,
                fuente_url,
                estado_revision,
                observaciones
            ) = fila


            if not nombre:
                continue


            cargador, creado = (
                CargadorElectrico.objects.update_or_create(
                    nombre=nombre,
                    direccion=direccion,
                    defaults={
                        "region": region,
                        "provincia": provincia,
                        "comuna": comuna,
                        "tipo_ubicacion": tipo_ubicacion,
                        "conectores_publicados":
                            conectores_publicados,
                        "tipo_conector":
                            tipo_conector,
                        "potencia_kw":
                            str(potencia_kw)
                            if potencia_kw is not None
                            else None,
                        "latitud": latitud,
                        "longitud": longitud,
                        "fuente_nombre":
                            fuente_nombre,
                        "fuente_url":
                            fuente_url,
                        "estado_revision":
                            estado_revision,
                        "observaciones":
                            observaciones,
                    }
                )
            )


            if creado:

                cargados += 1

            else:

                existentes += 1


        self.stdout.write(
            self.style.SUCCESS(
                f"Cargadores nuevos: {cargados}"
            )
        )

        self.stdout.write(
            self.style.WARNING(
                f"Cargadores ya existentes: {existentes}"
            )
        )