from django.db import models


class CargadorElectrico(models.Model):

    region = models.CharField(
        max_length=150,
        null=True,
        blank=True
    )

    provincia = models.CharField(
        max_length=150,
        null=True,
        blank=True
    )

    comuna = models.CharField(
        max_length=150,
        null=True,
        blank=True
    )

    tipo_ubicacion = models.CharField(
        max_length=150,
        null=True,
        blank=True
    )

    nombre = models.CharField(
        max_length=200
    )

    direccion = models.CharField(
        max_length=300,
        null=True,
        blank=True
    )

    conectores_publicados = models.CharField(
        max_length=200,
        null=True,
        blank=True
    )

    tipo_conector = models.CharField(
        max_length=200,
        null=True,
        blank=True
    )

    potencia_kw = models.CharField(
        max_length=100,
        null=True,
        blank=True
    )

    latitud = models.DecimalField(
        max_digits=10,
        decimal_places=7,
        null=True,
        blank=True
    )

    longitud = models.DecimalField(
        max_digits=10,
        decimal_places=7,
        null=True,
        blank=True
    )

    fuente_nombre = models.CharField(
        max_length=100,
        null=True,
        blank=True
    )

    fuente_url = models.URLField(
        max_length=500,
        null=True,
        blank=True
    )

    estado_revision = models.CharField(
        max_length=100,
        null=True,
        blank=True
    )

    observaciones = models.TextField(
        null=True,
        blank=True
    )

    def __str__(self):
        return f"{self.nombre} - {self.comuna}"
    