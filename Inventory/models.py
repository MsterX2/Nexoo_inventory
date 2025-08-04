from django.db import IntegrityError, models
from datetime import date
# Create your models here.


class Fecha(models.Model):
    """Tabla de fecha para registrar las fechas y hacer la logica de grapho para automatizar el orden de las fechas y acceder de forma mas eficiente a la fecha anterior"""
    fecha = models.DateField(
        unique=True,
        blank=True,
        null=True,
    )
    anterior = models.OneToOneField(
        'self',
        null=True,
        blank=True,
        related_name='siguiente',
        on_delete=models.DO_NOTHING
    )

    def supersave(self, *args, **kwargs):
        """Override save method to handle the date logic"""
        super(Fecha, self).save(*args, **kwargs)

    def save(self, *args, **kwargs):
        """Override save method to handle the date logic"""
        if Fecha.objects.filter(fecha=self.fecha).exists():
            raise IntegrityError("La fecha ya existe.")
        if not self.fecha:
            self.fecha = date.today()
        fecha_anterior = Fecha.objects.filter(
            fecha__lt=self.fecha).order_by('-fecha').first()
        fecha_siguiente = Fecha.objects.filter(
            fecha__gt=self.fecha).order_by('fecha').first()
        if fecha_siguiente:
            fecha_siguiente.anterior = self
            self.anterior = fecha_anterior
            fecha_siguiente.supersave()
        elif fecha_anterior:
            self.anterior = fecha_anterior
        super().save(*args, **kwargs)

    def __str__(self):
        return str(self.fecha)


class FechaField(models.Model):
    """
    Clase abstracta para asignarle una llave foranea a la tabla de fechas
    Esta clase es estrictamente para la clase de inventario principal
    """
    fecha = models.OneToOneField(
        Fecha,
        on_delete=models.RESTRICT,
        related_name='inventario'
    )

    class Meta:
        abstract = True


class Producto(models.Model):
    "tabla de Productos"
    nombre = models.CharField(max_length=50)
    valor_compra = models.DecimalField(decimal_places=2, max_digits=10)
    valor_venta = models.DecimalField(decimal_places=2, max_digits=10)
    default_stock = models.DecimalField(decimal_places=0, max_digits=10)
    base = models.ForeignKey(
        'self',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='variantes'

    )

    def __str__(self):
        return self.nombre


class Inventory(FechaField):
    """Tabla para registrar inventarios con sus fechas"""

    def __str__(self):
        return f"Inventario de {self.fecha.fecha}"


class InventoryProducto(models.Model):
    nombre = models.ForeignKey(Producto, on_delete=models.RESTRICT)
    inventario = models.ForeignKey(
        Inventory,
        on_delete=models.RESTRICT,
        related_name='productos',
    )
    stock = models.DecimalField(
        decimal_places=2, default=0, blank=True, max_digits=10)
