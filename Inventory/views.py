from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from .models import Fecha, Inventory, Producto
# Create your views here.


def index(request):
    inventario = Inventory.objects.get(fecha=Fecha.objects.latest('fecha'))
    productos = inventario.productos.select_related(
        'nombre', 'inventario__fecha').all().order_by('nombre_id')
    return render(
        request,
        'index.html',
        context={'inventario': inventario, 'productos': productos}
    )


def detalle(request, nombre_id):
    producto = get_object_or_404(Producto, id=nombre_id)
    return render(
        request,
        'detalle.html',
        context={'producto': producto}
    )
