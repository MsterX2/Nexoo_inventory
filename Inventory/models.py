from django.db import models
from datetime import date
# Create your models here.


class Fecha(models.Model):
    """Tabla de fecha para registrar las fechas y hacer la logica de grapho para automatizar el orden de las fechas y acceder de forma mas eficiente a la fecha anterior"""
    fecha = models.DateField(
        unique=True,
        blank=True,
        null=True,
    )

    def save(self, *args, **kwargs):
        if not self.fecha:
            self.fecha = date.today()
        super().save(*args, **kwargs)

    def __str__(self):
        return str(self.fecha)


class FechaField(models.Model):
    """Clase abstracta para asignarle una llave foranea a la tabla de fechas"""
    fecha = models.ForeignKey(
        Fecha,
        on_delete=models.CASCADE,
        blank=True,
        null=True,
    )

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        if self.fecha is None:
            self.fecha, _ = Fecha.objects.get_or_create(fecha=date.today())
        super().save(*args, **kwargs)


class Producto(models.Model):
    "tabla de Productos"
    nombre = models.CharField(max_length=50)
    valor_compra = models.FloatField()
    valor_venta = models.FloatField()
    base = models.ForeignKey(
        'self',
        null=True,
        blank=True,
        on_delete=models.SET_NULL
    )

    def __str__(self):
        return self.nombre


class Categoria(FechaField, models.Model):
    nombre = models.CharField(max_length=50)
    producto = models.ForeignKey(
        Producto,
        on_delete=models.RESTRICT,
        related_name='categoria'
    )
    stock = models.FloatField()


class Inventory(FechaField):

    nombre = models.ForeignKey(Producto, on_delete=models.CASCADE)
    stock = models.FloatField()
