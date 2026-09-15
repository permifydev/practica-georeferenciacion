# Create your models here.
from django.db import models


class VehiculoElectrico(models.Model):

    marca = models.CharField(
        max_length=100
    )

    modelo = models.CharField(
        max_length=100
    )

    version = models.CharField(
        max_length=100
    )

    bateria_kwh = models.DecimalField(
        max_digits=6,
        decimal_places=2
    )

    autonomia_km = models.DecimalField(
        max_digits=7,
        decimal_places=2
    )

    tiempo_carga_10_80_min = models.PositiveIntegerField(
    null=True,
    blank=True
    )

    detalle_carga = models.CharField(
    max_length=200,
    null=True,
    blank=True
    )

    def __str__(self):
        return f"{self.marca} {self.modelo} {self.version}"