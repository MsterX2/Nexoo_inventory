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
    path('form/producto', views.formulario_producto, name='formulario'),
    path('form/inventario', views.formulario_inventario, name='inventory_form'),
    path('form/fecha', views.formulario_fecha, name='fecha_form'),
]
