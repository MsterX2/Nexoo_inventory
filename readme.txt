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