Despliegue en producción
========================

Para facilitar el despliegue en un entorno de producción se proporciona un
script para facilitar esta tarea.

El script llamado `autodeploy.sh` es un script automatizado para el despliegue
en producción en servidores Linux basados en Ubuntu/Debian. Antes de ejecutar
el script debe asegurarse de configurarlo correctamente. 

A continuación se muestran las variables configurables del script:

.. attribute:: PYTHON_VERSION='3.7'

   Versión de Python que se usó en el desarrollo del proyecto y que se
   instalará durante el despliegue. No se debe cambiar a menos que el proyecto
   cambie.

.. attribute:: PROJECT_NAME='unicauca_vrcb'

   Nombre del proyecto actual. No se debe cambiar a menos que el proyecto
   cambie.

.. attribute:: BASE_PATH=`pwd`

   Ruta absoluta a la ubicación donde recidirá el código fuente del sistema. No
   se debe modificar a menos que se ejecute el script desde una ubicación
   diferente.

.. attribute:: DUMP_FILE=''

   Nombre del archivo de volcado de base de datos que llenará la base de datos
   con datos de ejemplo. No se debe usar en producción a menos que se trate
   de una operación de restauración de una copia de seguridad. 

   .. note::

      También debe quitar el comentario de la línea 29 del código fuente del
      script para que el llenado de la base de datos se ejecute.

.. attribute:: STATIC_PATH='static'

   Nombre del directorio donde se almacenarán los archivos estáticos (css, js,
   imagenes, etc.).

.. attribute:: MEDIA_URL='media'

   URL desde donde se servirán lo archivos subidos por los clientes.

.. attribute:: MEDIA_PATH='media'

   Nombre del directorio donde se almacenarán los archivos subidos por los
   clientes.

.. attribute:: APP_PORT=80

   Número del puerto a través del cual el servidor aceptará solicitudes. Por favor, no cambie este valor a menos que sepa lo que hace. Recuerde que la aplicación móvil que acompaña a este cliente se conectará a este sistema a
   través de este puerto.

.. attribute:: DOMAINS=''

   Dominio o dominios permitidos para hacer consultas al sistema. Agregue nombres de dominio, host e IP's que se conectarán a este sistema. Separe
   cada host por un espacio.

.. attribute:: MAX_UPLOAD='10M'

   Tamaño máximo de subida de archivos.

.. attribute:: PROXY_PASS='http://unix:'$BASE_PATH'/'$PROJECT_NAME'.sock'

   Tipo de proxy que se usará para enlazar el servidor web `NGINX` con el
   servidor WSGI `Gunicorn`. Para mayor información visite:
   http://docs.gunicorn.org/en/stable/.

.. attribute:: GUNICORN_SERVICE_USER=$USER

   Nombre del usuario del sistema operativo sobre el cual se desplegará la aplicación. De forma predefinida se desplegará sobre el usuario actual.

Para un despliegue rápido solo debe configurar la variable ``DOMAINS``.

El script de despliegue también intentará generar y configurar el certificado
SSL para el sistema. El certificado le permite servir el sistema a través de
HTTPS de forma segura, también es fundamental para el funcionamiento óptimo de
las aplicaciones móviles que se conectan con el sistema. El certificado tiene
una validez de 3 meses y se actualizará automáticamente una semana antes de
llegada la fecha de expiración.

Por último, al final del script se proporcionan algunos comando útiles que le
permitirán revisar que el despliegue se ha realizado correctamente.

.. warning::

   Recuerde que antes de ejecutar el script de despliegue debe poner en
   comentario o borrar la ruta ``admin/`` del archivo de rutas.

Para ejecutar el script de despliegue ejecute el siguiente comando en una
terminal:


.. code-block:: bash
   :linenos:

   sudo ./autodeploy.sh