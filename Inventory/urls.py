from django.urls import path
from . import views
app_name = 'Inventory'
urlpatterns = [
    path('', views.index, name='index'),
    path('productos/<int:nombre_id>', views.detalle, name='detalle'),
    path('inventarios/diferencia/<int:inventario_id>', views.obtener_diferencia_inventario,
         name='diferencia_inventario'),
    path('listar/', views.listar_modelos, name='listar_modelos'),
    path('listar/<str:model_name>', views.listar, name='listar_modelo'),
    path('form/<str:model_name>', views.model_forms, name="formularios"),
    path('form/formset/InventarioProucto', views.form_set_model, name='formset')
]
