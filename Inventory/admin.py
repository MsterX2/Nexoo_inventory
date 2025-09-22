from django.contrib import admin
from .models import Factura, FacturasCompra, FacturasVenta, InventoryProducto, Fecha, Producto, Inventory


class InventoryProductoAdmin(admin.ModelAdmin):
    list_display = ('id', 'producto', 'stock', 'inventario')
    list_display_links = ('inventario',)
    list_filter = ('inventario__fecha__fecha',)
    list_select_related = ('producto', 'inventario')
    list_editable = ('stock',)


admin.site.register(Fecha)
admin.site.register(Producto)
admin.site.register(Inventory)
admin.site.register(InventoryProducto, InventoryProductoAdmin)
admin.site.register(Factura)
admin.site.register(FacturasCompra)
admin.site.register(FacturasVenta)
