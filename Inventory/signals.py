from django.dispatch import receiver
from django.db.models.signals import pre_delete, post_save
from .models import Fecha, InventoryProducto
from django.db.models import Sum


@receiver(pre_delete, sender=Fecha)
def reasignar_fecha_anterior(sender, instance, **kwargs):
    if instance.siguiente:
        instance.siguiente.anterior = instance.anterior
        instance.siguiente.supersave()


@receiver(post_save, sender=InventoryProducto)
def asignar_stock_de_producto_generico(sender, instance, **kwargs):
    generico = instance.nombre.base
    if generico:
        InventoryProducto.objects.update_or_create(inventario=instance.inventario,
                                                   nombre=generico,
                                                   defaults=InventoryProducto.objects.filter(
                                                       nombre__in=generico.variantes.all(),
                                                       inventario=instance.inventario).aggregate(
                                                       stock=Sum('stock')))
