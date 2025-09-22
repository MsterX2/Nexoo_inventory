from django.forms import modelform_factory
from django.apps import apps
from django import forms


formularios = {}
widgets_definidos = {
    'DateField': forms.DateInput(attrs={'type': 'date'}),
    'inventario': forms.TextInput(attrs={'readonly': True})
}


def form(modelo=None, widgets_list=None, widgets_extra=None, fields="__all__", exclude=None):
    if modelo in formularios:
        return formularios[modelo]
    else:
        modelo = apps.get_model("Inventory", modelo)
        widgets_list = widgets_list or []
        widgets_list = [field.get_internal_type() for field in modelo._meta.get_fields(
        ) if field.get_internal_type() in widgets_definidos]
        if widgets_list:
            widgets_extra = widgets_extra or {}
            widgets_extra = {**{
                key: value for key, value in widgets_definidos.items() if key in widgets_list}, **widgets_extra}
    # formularios[modelo] = modelform_factory(model=modelo,
    #                                         fields=include,
    #                                         exclude=exclude,
    #                                         widgets=widgets_extra
    #                                         )
    # return formularios[modelo]
    return modelform_factory(model=modelo,
                             fields=fields,
                             exclude=exclude,
                             widgets={'inventario': forms.TextInput(
                                 attrs={'readonly': True}), },
                             )
