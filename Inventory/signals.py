from django.dispatch import receiver
from django.db.models.signals import pre_delete, post_save
from .models import Inventory, InventoryProducto
from django.db.models import Sum

from django.db import transaction


@receiver(post_save, sender=Inventory)
def actualizar_inventario_anterior_y_siguiente(sender, instance, created, **kwargs):
    with transaction.atomic():
        if created:
            anterior = Inventory.objects.filter(
                fecha__fecha__lt=instance.fecha.fecha).order_by('-fecha__fecha').first()
            siguiente = Inventory.objects.filter(
                fecha__fecha__gt=instance.fecha.fecha).order_by('fecha__fecha').first()
            if anterior:
                instance.anterior = anterior
                anterior.siguiente = instance
                anterior.save(**kwargs)
            if siguiente:
                instance.siguiente = siguiente
                siguiente.anterior = instance
                siguiente.save(**kwargs)
            instance.save(**kwargs)


@receiver(pre_delete, sender=Inventory)
def actualizar_inventario_anterior_y_siguiente(sender, instance, **kwargs):
    with transaction.atomic():
        if instance.anterior:
            instance.anterior.siguiente = instance.siguiente
            instance.anterior.save(**kwargs)
            instance.anterior = None
        if instance.siguiente:
            instance.siguiente.anterior = instance.anterior
            instance.siguiente.save(**kwargs)
            instance.siguiente = None


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
