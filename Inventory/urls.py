from django.urls import path
from . import views
app_name = 'Inventory'
urlpatterns = [
    path('', views.index, name='index'),
    path('productos/<int:nombre_id>', views.detalle, name='detalle'),
    path('productos', views.listar_productos, name='listar_productos'),
    path('inventarios', views.listar_inventarios, name='listar_inventarios'),
    path('inventarios/diferencia/<int:inventario_id>', views.obtener_diferencia_inventario,
         name='diferencia_inventario'),
    path('formularios', views.formularios, name='formularios'),
    path('form/producto', views.formulario_producto, name='formulario'),
    path('form/inventario', views.formulario_inventario, name='inventory_form'),
    path('form/fecha', views.formulario_fecha, name='fecha_form'),
    path('form/factura', views.formulario_factura, name='factura_form'),
    path('form/factura_de_compra', views.formulario_factura_compra,
         name='factura_compra_form'),
    path('form/factura_de_venta ', views.formulario_factura_venta,
         name='factura_venta_form'),
    path('form/inventario_producto',
         views.formulario_inventario_producto, name='inventario_producto'),
    path('listar', views.listar, name='listar')
]
