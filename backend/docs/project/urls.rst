Configuración de rutas
======================

El archivo ``urls.py`` ubicado en ``unicauca_vrcb`` contiene la lista de rutas
permitidas en el sistema. Para más información sobre los patrones de rutas visite: https://docs.djangoproject.com/en/2.1/topics/http/urls/

Al estar separados el backend de cada uno de sus clientes (web y apps móviles),
el sistema solo tiene una ruta accesible: la ruta ``raíz``.

A través de la ruta raíz se servirá el API GraphQL que permite a los clientes
conectarse e interactuar con el sistema.

También se incluye la ruta ``admin/`` la cual permite el acceso a la interfaz
administrativa de Django. Recuerde que la interfaz administrativa solo debe ser
usada en un ambiente de desarrollo.

.. note::

   Recuerde comentar la ruta ``admin/`` del archivo de rutas cuando realice el
   despliegue en producción.