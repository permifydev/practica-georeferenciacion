from django.core.management.base import BaseCommand

from electromovilidad.models import VehiculoElectrico


class Command(BaseCommand):

    help = "Carga los vehículos eléctricos iniciales"

    def handle(self, *args, **options):

        vehiculos = [
            {
                "marca": "Volvo",
                "modelo": "EX30",
                "version": "CORE E40",
                "bateria_kwh": 51,
                "autonomia_km": 344,
                "tiempo_carga_10_80_min": 26,
                "detalle_carga": "Carga 10-80% en 26 minutos"
            },
            {
                "marca": "Volvo",
                "modelo": "EX30",
                "version": "PLUS E60",
                "bateria_kwh": 69,
                "autonomia_km": 480,
                "tiempo_carga_10_80_min": 27,
                "detalle_carga": "Carga 10-80% en 27 minutos"
            },
            {
                "marca": "Volvo",
                "modelo": "EX30",
                "version": "ULTRA E60",
                "bateria_kwh": 69,
                "autonomia_km": 480,
                "tiempo_carga_10_80_min": 27,
                "detalle_carga": "Carga 10-80% en 27 minutos"
            },
            {
                "marca": "BMW",
                "modelo": "i4",
                "version": "eDrive40 M Sport LCI II",
                "bateria_kwh": 81.3,
                "autonomia_km": 600,
                "tiempo_carga_10_80_min": 30,
                "detalle_carga": "Carga rápida DC 10-80% en 30 min a 205 kW"
            },
            {
                "marca": "Audi",
                "modelo": "Q6 e-tron",
                "version": "Base",
                "bateria_kwh": 75.8,
                "autonomia_km": 533,
                "tiempo_carga_10_80_min": None,
                "detalle_carga": "Carga AC 0-100% en 480 min"
            },
            {
                "marca": "Audi",
                "modelo": "Q6 e-tron",
                "version": "quattro",
                "bateria_kwh": 94.9,
                "autonomia_km": 622,
                "tiempo_carga_10_80_min": None,
                "detalle_carga": "Carga AC 0-100% en 600 min"
            },
            {
                "marca": "Audi",
                "modelo": "Q6 e-tron",
                "version": "performance",
                "bateria_kwh": 94.9,
                "autonomia_km": 639,
                "tiempo_carga_10_80_min": None,
                "detalle_carga": "Carga AC 0-100% en 615 min"
            },
            {
                "marca": "Tesla",
                "modelo": "Model Y",
                "version": "RWD",
                "bateria_kwh": 60,
                "autonomia_km": 554,
                "tiempo_carga_10_80_min": None,
                "detalle_carga": "Carga rápida 20-80% en 60 min"
            },
            {
                "marca": "Tesla",
                "modelo": "Model Y",
                "version": "Long Range 4WD",
                "bateria_kwh": 78.4,
                "autonomia_km": 688,
                "tiempo_carga_10_80_min": None,
                "detalle_carga": "Carga rápida 20-80% en 60 min"
            },
            {
                "marca": "Hyundai",
                "modelo": "KONA EV",
                "version": "SX2 EV GO",
                "bateria_kwh": 48.6,
                "autonomia_km": 370,
                "tiempo_carga_10_80_min": None,
                "detalle_carga": "Carga rápida 0-80% aprox. 45 min con cargador 100 kW"
            },
            {
                "marca": "Hyundai",
                "modelo": "KONA EV",
                "version": "SX2 EV GO LR",
                "bateria_kwh": 64.8,
                "autonomia_km": 505,
                "tiempo_carga_10_80_min": None,
                "detalle_carga": "Carga rápida 0-80% aprox. 45 min con cargador 100 kW"
            },
            {
                "marca": "Tesla",
                "modelo": "Model 3",
                "version": "Standard Range",
                "bateria_kwh": 50,
                "autonomia_km": 423,
                "tiempo_carga_10_80_min": None,
                "detalle_carga": "La ficha no informa tiempo de carga 10-80%"
            },
            {
                "marca": "BMW",
                "modelo": "i5",
                "version": "eDrive40 2025",
                "bateria_kwh": 81.2,
                "autonomia_km": 498,
                "tiempo_carga_10_80_min": None,
                "detalle_carga": "Carga 0-100% en 11 horas con Wallbox de 7.4 kW"
            }
        ]

        creados = 0
        existentes = 0

        for vehiculo in vehiculos:

            objeto, creado = VehiculoElectrico.objects.get_or_create(
                marca=vehiculo["marca"],
                modelo=vehiculo["modelo"],
                version=vehiculo["version"],
                defaults={
                    "bateria_kwh": vehiculo["bateria_kwh"],
                    "autonomia_km": vehiculo["autonomia_km"],
                    "tiempo_carga_10_80_min": vehiculo[
                        "tiempo_carga_10_80_min"
                    ],
                    "detalle_carga": vehiculo["detalle_carga"]
                }
            )

            if creado:
                creados += 1
            else:
                existentes += 1

        self.stdout.write(
            self.style.SUCCESS(
                f"Vehículos creados: {creados}. "
                f"Vehículos existentes: {existentes}."
            )
        )