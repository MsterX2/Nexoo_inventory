from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from .models import Fecha, Inventory, Producto
from .forms import ProductoForm
# Create your views here.


def index(request):
    inventario = Inventory.objects.get(fecha=Fecha.objects.latest('fecha'))
    productos = inventario.productos.select_related(
        'producto', 'inventario__fecha').all().order_by('producto_id')
    return render(
        request,
        'index.html',
        context={'inventario': inventario, 'productos': productos}
    )


def listar_inventarios(request):
    inventarios = Inventory.objects.all().order_by('-fecha__fecha')
    return render(
        request,
        'inventarios.html',
        context={'inventarios': inventarios}
    )


def listar_productos(request):
    productos = Producto.objects.all().order_by('-base')
    return render(
        request,
        'productos.html',
        context={'productos': productos}
    )


def detalle(request, nombre_id):
    producto = get_object_or_404(Producto, id=nombre_id)
    return render(
        request,
        'detalle.html',
        context={'producto': producto}
    )


def formulario_producto(request):
    if request.method == 'POST':
        form = ProductoForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect("")
    else:
        form = ProductoForm()
    return render(request, 'form/producto_form.html', {'form': form})


def formulario_inventario(request):
    from .forms import InventoryForm
    if request.method == 'POST':
        form = InventoryForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect("")
    else:
        form = InventoryForm()
    return render(request, 'form/inventory_form.html', {'form': form})


def formulario_fecha(request):
    from .forms import FechaForm
    if request.method == 'POST':
        form = FechaForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect("")
    else:
        form = FechaForm()
    return render(request, 'form/fecha_form.html', {'form': form})


def obtener_diferencia_inventario(request, inventario_id):
    from .workspace.pruebas import obtener_diferencia_inventario
    inventario = get_object_or_404(
        Inventory, id=inventario_id)
    inventario = obtener_diferencia_inventario(inventario.fecha.fecha)
    return render(
        request,
        'diferencia.html',
        context={'inventario': inventario}
    )


def formulario_factura(request):
    from .forms import FacturaForm
    if request.method == 'POST':
        form = FacturaForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect("")
    else:
        form = FacturaForm()
    return render(request, 'form/factura_form.html', {'form': form})


def formulario_factura_compra(request):
    from .forms import FacturasCompraForm
    if request.method == 'POST':
        form = FacturasCompraForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect("")
    else:
        form = FacturasCompraForm()
    return render(request, 'form/factura_compra_form.html', {'form': form})


def formulario_factura_venta(request):
    from .forms import FacturasVentaForm
    if request.method == 'POST':
        form = FacturasVentaForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect("")
    else:
        form = FacturasVentaForm()
    return render(request, 'form/factura_venta_form.html', {'form': form})


def formulario_inventario_producto(request):
    from .forms import InventoryProductoForm
    if request.method == 'POST':
        form = InventoryProductoForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect("inventario_producto")
    else:
        form = InventoryProductoForm()
    inventario_default = Inventory.objects.order_by(
        'fecha').last()
    inventario_default = inventario_default.anterior
    form.fields["inventario"].initial = inventario_default.id
    return render(request, 'form/inventario_producto.html', {'form': form})


def formularios(request):
    return render(request, 'formularios.html')
