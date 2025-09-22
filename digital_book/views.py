from django.apps import apps
from django.shortcuts import render


def inicio(request):
    modelos = apps.get_app_config('Inventory').get_models()
    modelos = [model.__name__ for model in modelos]
    return render(request, 'inicio.html', {"modelos": modelos})
