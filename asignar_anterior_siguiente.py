import os
import django

# 👇 Ajusta con el nombre correcto del settings.py de tu proyecto
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Nexoo_inventory.settings')

django.setup()


inventarios = Inventory.objects.all().order_by('fecha')
for inventario in inventarios:
    print(inventario)
