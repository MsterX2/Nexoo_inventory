from . import models
from django.forms import ModelForm, modelform_factory
from django import forms


class ProductoForm(ModelForm):
    class Meta:
        model = models.Producto
        fields = ['nombre', 'default_stock', 'base']


class InventoryForm(ModelForm):
    class Meta:
        model = models.Inventory
        fields = ['fecha']


class InventoryProductoForm(ModelForm):
    class Meta:
        model = models.InventoryProducto
        fields = ['producto', 'inventario', 'stock']


class FacturaForm(ModelForm):
    class Meta:
        model = models.Factura
        fields = ['inventario', 'fecha']
        widgets = {
            'fecha': forms.DateInput(attrs={'type': 'date'})
        }


class FacturasCompraForm(ModelForm):
    class Meta:
        model = models.FacturasCompra
        fields = ['stock', 'monto', 'factura', 'producto']


class FacturasVentaForm(ModelForm):
    class Meta:
        model = models.FacturasVenta
        fields = ['stock', 'monto', 'factura', 'producto']


class FechaForm(ModelForm):
    class Meta:
        model = models.Fecha
        fields = ['fecha']
        widgets = {
            'fecha': forms.DateInput(attrs={'type': 'date'})
        }
