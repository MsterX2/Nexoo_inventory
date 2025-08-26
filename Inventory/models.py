from django.db import IntegrityError, models
from datetime import date
# Create your models here.


class Fecha(models.Model):
    """Tabla de fecha para registrar las fechas y hacer la logica de grapho para automatizar el orden de las fechas y acceder de forma mas eficiente a la fecha anterior"""
    fecha = models.DateField(
        unique=True,
    )

    def __str__(self):
        return str(self.fecha)


class Producto(models.Model):
    "tabla de Productos"
    nombre = models.CharField(max_length=50)
    default_stock = models.DecimalField(
        decimal_places=0, max_digits=10, default=0)
    base = models.ForeignKey(
        'self',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='variantes'

    )

    def __str__(self):
        return self.nombre


class Inventory(models.Model):
    """Tabla para registrar inventarios con sus fechas"""
    fecha = models.OneToOneField(
        Fecha,
        on_delete=models.RESTRICT,
        related_name='inventario'
    )
    anterior = models.OneToOneField(
        'self', null=True, blank=True, on_delete=models.DO_NOTHING, related_name='+')
    siguiente = models.OneToOneField(
        'self', null=True, blank=True, on_delete=models.DO_NOTHING, related_name='+')

    def __str__(self):
        return f"Inventario de {self.fecha.fecha}"


class InventoryProducto(models.Model):
    producto = models.ForeignKey(
        Producto, on_delete=models.RESTRICT, related_name='inventarios')
    inventario = models.ForeignKey(
        Inventory,
        on_delete=models.RESTRICT,
        related_name='productos',
    )
    stock = models.DecimalField(
        decimal_places=2, default=0, blank=True, max_digits=10)

    def __str__(self):
        return f"{self.nombre.nombre} - {self.inventario.fecha.fecha} - {self.stock}"


class Factura(models.Model):
    """Tabla para registrar las facturas"""
    inventario = models.ForeignKey(
        Inventory,
        on_delete=models.RESTRICT,
        related_name='facturas',
    )
    fecha = models.OneToOneField(
        Fecha,
        on_delete=models.RESTRICT,
        related_name='factura'
    )


class FacturasDatafield(models.Model):
    stock = models.DecimalField(
        decimal_places=0, default=0, blank=True, max_digits=10)
    monto = models.DecimalField(
        decimal_places=2, default=0, blank=True, max_digits=10)

    class Meta:
        abstract = True


class FacturasCompra(FacturasDatafield):
    """Tabla para registrar las facturas"""
    factura = models.ForeignKey(
        Factura,
        on_delete=models.RESTRICT,
        related_name='compras',
    )
    producto = models.ForeignKey(
        Producto,
        on_delete=models.RESTRICT,
        related_name='compras',
    )


class FacturasVenta(FacturasDatafield):
    """Tabla para registrar las facturas"""
    factura = models.ForeignKey(
        Factura,
        on_delete=models.RESTRICT,
        related_name='ventas',
    )
    producto = models.ForeignKey(
        Producto,
        on_delete=models.RESTRICT,
        related_name='ventas',
    )
