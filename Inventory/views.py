from django.apps import apps
from django.forms import inlineformset_factory
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from .models import Fecha, Inventory, InventoryProducto, Producto
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


def detalle(request, nombre_id):
    producto = get_object_or_404(Producto, id=nombre_id)
    return render(
        request,
        'detalle.html',
        context={'producto': producto}
    )


def obtener_diferencia_inventario(request, inventario_id):
    from .workspace.pruebas import obtener_diferencia_inventario
    from django.db.models import Q
    inventario = get_object_or_404(
        Inventory, id=inventario_id)
    inventario = obtener_diferencia_inventario(inventario.fecha.fecha)
    inventario = inventario.filter(~Q(inventario_anterior_compras=0) &
                                   ~Q(inventario_actual_ventas=0))
    return render(
        request,
        'diferencia.html',
        context={'inventario': inventario}
    )


def listar(request, model_name):
    modelo = apps.get_model('Inventory', model_name)
    qs = modelo.objects.all().select_related().order_by()
    fields = modelo._meta.fields
    modelo_dicts = [{field.name: getattr(objeto, field.name) for field in fields}
                    for objeto in qs]
    return render(
        request,
        "listar.html",
        {
            'var': '_listar.html',
            'modelo_dicts': modelo_dicts,
            'fields': fields,
            'name': model_name,
        }
    )


def listar_modelos(request):
    modelos = apps.get_app_config('Inventory').get_models()
    modelos = [model.__name__ for model in modelos]
    return render(request, "listar.html", {
        'var': 'inicio.html',
        'modelos': modelos,
        'url_actual': 'Inventory:listar_modelo',
        'name': 1,
        'Tittle': 'Listar Modelos',
    })


def model_forms(request, model_name):
    from .forms import form

    Form = form(model_name)

    form = Form(request.POST or None)
    if request.method == "POST" and form.is_valid():
        form.save()
        return HttpResponseRedirect('')
    return render(
        request,
        "form/form.html",
        {
            'form': form,
            'model': model_name,
        }
    )


def form_set_model(request):
    from .forms import form
    fechas = tuple(Inventory.objects.order_by(
        'fecha__fecha').values_list('fecha__fecha', flat=True))

    def get_padre(fechas):
        """Devuelve el modelo padre Inventory según las fechas dadas"""
        return Inventory.objects.order_by('fecha__fecha').filter(fecha__fecha__in=fechas)

    def get_inlineformset(padre, hijo, ModelForm, fields):
        """Devuelve un inlineformset para los modelos dados"""
        return inlineformset_factory(
            padre,
            hijo,
            fields=fields,
            form=ModelForm,
            extra=0,
            can_delete=True
        )

    campos = InventoryProducto.objects.filter(inventario__fecha__fecha__in=fechas).order_by(
        'producto').values_list('producto__nombre', flat=True).distinct()
    padres = get_padre(fechas)
    hijo = InventoryProducto
    fields = ['producto', 'inventario', 'stock']
    ModelForm = form(modelo=hijo.__name__, fields=fields)
    FormSetModel = get_inlineformset(Inventory, hijo, ModelForm, fields)

    formsets = [FormSetModel(
        request.POST or None, instance=padre) for padre in padres]
    """Crear un diccionario con los formularios organizados por producto y fecha"""
    table = {campo: {fecha: None for fecha in fechas} for campo in campos}

    def empty_form(producto, fecha):
        low, high = 0, len(formsets) - 1
        formset = None
        while low <= high:
            mid = (low + high) // 2
            if formsets[mid].instance.fecha.fecha == fecha:
                formset = formsets[mid]
                break
            if formsets[mid].instance.fecha.fecha < fecha:
                low = mid + 1
            else:
                high = mid
        formset_vacio = formset.empty_form
        formset_vacio.initial = {'producto': producto}
        return formset_vacio

    for formset in formsets:
        for form in formset:
            table[form.instance.producto.nombre][form.instance.inventario.fecha.fecha] = form
    table = {producto: {fecha: value if value else empty_form(
        producto, fecha) for fecha, value in fechas.items()} for producto, fechas in table.items()}

    if request.method == 'POST' and all(fs.is_valid() for fs in formsets):
        for formset in formsets:
            formset.save()
        return HttpResponseRedirect('')

    return render(
        request,
        'form/formset.html',
        {
            'table': table,
            'fechas': fechas,
        }
    )
