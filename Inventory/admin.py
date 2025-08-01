from django.contrib import admin
from .models import Categoria, Fecha, Producto, Inventory
# Register your models here.
admin.site.register(Inventory)
admin.site.register(Fecha)
admin.site.register(Producto)
admin.site.register(Categoria)
