from . import models
from django.forms import ModelForm
from django import forms


class ProductoForm(ModelForm):
    class Meta:
        model = models.Producto
        fields = ['nombre', 'default_stock', 'base']


class InventoryForm(ModelForm):
    class Meta:
        model = models.Inventory
        fields = ['fecha']


class FechaForm(ModelForm):
    class Meta:
        model = models.Fecha
        fields = ['fecha']
        widgets = {
            'fecha': forms.DateInput(attrs={'type': 'date'})
        }
