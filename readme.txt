*Iniciar proyecto*
en shell
django-admin startproject [nombre del proyecto] .

*crear aplicacion dentro del proyecto*
en shell
python manage.py startapp [nombre de la aplicacion]

*Crear vinculo con la app*
en [dir de proyecto]/settings.py
    en apps instaladas agregar:
        [nombre de aplicacion].apps.[nombre de aplicacion]Config
en [dir de proyecto]/urls.py
    agregar en urlpatterns:
        path('[nombre de la direccion url a registrar]',
             include('[nombre de la aplicacion].urls'))
dentro del dir de la aplicacion crear archivo urls.py con el siguiente texto:
    from django.urls import path
    from . import [path del archivo donde se encuentra la funcion]

    urlpatterns = [
        path([path desde donde ya nos encontramos en el dir de la app],
            [path de la funcion separado por puntos],
             name='[nombre para futura referencia]')
    ]
*Modelos llave foranea on_delete:*
CASCADE -> elimina el objeto
PROTECT -> impide que se elimine el objeto mientras tenga otros elementos referenciandolo lanzando un error
RESTRICT -> no deja eliminar mientras tenga asociados
SET_NULL -> vuelve null el campo
SET_DEFAULT -> lo convierte en el valor por defecto
DO_NOTHING -> no hace nada
SET() -> decide manualmente que sucede

*migraciones, reflejar los modelos en la base de datos*
en shell
python manage.py makemigrations
python manage.py migrate

*Crear administrador*
python manage.py createsuperuser

*Interactuar con la orm*
model.objects. -> (all, get, filter)
argumentos
nomnre del campo si se le quiere aplicar algun metodo extra usar __ y el nombre
gt -> mayor que
lt -> menor  que
gte -> mayor o igual que
lte -> menor  o igual que


*renderizando plantillas html*
en view usar:
returm render (
    request,
    plantillas_name,
    context -> variables en diccionario

)

*Extender de archivos html*
{% extends "base.html" %}
{% block content %}
{% end block content %}


***formularios***
from . import models
from django.forms import ModelForm


class ProductoForm(ModelForm):
    class Meta:
        model = modelo del cual se va a crear el formulario
        fields = listas de campos del modelo

em view

def formulario(request):
    form = ProductoForm()
    return render(request, 'producto_form.html', {'form': form})


en plantilla html

{% block content %}
  <h2>Agregar Producto</h2>
  <form action="{% url "Inventory:formulario" %}" method="post">
    {% csrf_token %} -> nunca olvidar poner sirve para mejor seguridad

    {{ form }}
    <button type="submit">Guardar</button>
  </form>
{% endblock content %}



***validando el formulario***
def formulario(request):
    if request.method == 'POST':
        form = ProductoForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect("/Inventory")
    else:
        form = ProductoForm()
    return render(request, 'producto_form.html', {'form': form})


***personalizar formularios
    from django.forms.renderers import TemplatesSetting


class CustomFormRenderer(TemplatesSetting):
    form_template_name = 'form_snippet.html'


FORM_RENDERER = "nombre del proyecto.settings.CustomFormRenderer"


***personalizando campos en formularios***
crear templates/django/forms/widgets/input.html
y agregar el texto 

<input 
    class="form-control"
    type="{{ widget.type }}" 
    name="{{ widget.name }}"
    {% if widget.value != None %} value="
    {{ widget.value|stringformat:'s' }}"
     {% endif %}
     {% include "django/forms/widgets/attrs.html" %}>

"""
Archivo form_snippet
{% load add_attr %}

{% for field in form %}
    <div class="mb-3">
        {{field.label_tag}} 
        {% if field.errors %}
            {{ field|add_attr:"class:is-invalid" }}
        {% else %}
            {{ field }}
        {% endif %}
        <div  class="invalid-feedback">
        {% for error in field.errors %}
            {{error}}
            {% endfor %}
        </div>
    </div>
{% endfor %}
"""
***definir atributo***
from django import template
register = template.Library()


@register.filter(name="add_attr")
def add_attr(field, css):
    attrs = {}
    clase, valor = css.split(':')
    attrs[clase] = valor
    return field.as_widget(attrs=attrs)

"""

***Pagina de inicio***
