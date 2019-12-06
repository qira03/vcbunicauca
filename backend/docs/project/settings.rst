Configuración
=============
Configuración global del proyecto generada automáticamente por Django 2.1.3.

Para más información sobre este archivo visite:
https://docs.djangoproject.com/en/2.1/topics/settings/.

Para una lista completa de configuraciones y sus valores visite:
https://docs.djangoproject.com/en/2.1/ref/settings/.

.. attribute:: SECRET_KEY

   Clave secreta para una instancia del sistema. Es usada para el aseguramiento
   de las sesiones, mensajes a los clientes y cualquier firma criptográfica,
   debe ser única e impredecible.

   .. warning::

      Cambie el valor cuando pase a producción y manténgala secreta.

.. attribute:: DEBUG

   Booleano que activa o inactiva el modo de depuración. Si el su valor es
   `True` se motrará un seguimiento detallado de las excepciones ocurridas en
   el sistema.

   .. warning::

      Nunca despliegue el proyecto en producción con DEBUGen True.

.. attribute:: ALLOWED_HOSTS

   Lista de nombres de host, dominios o IP's a los que el sistema puede
   responder solicitudes. Esta es una medida de seguridad para evitar ataques
   de encabezado de Host HTTP.

   .. note::

      Cuando despliegue el proyecto en producción asegúrese de agregar los
      nombres de dominio o IP's adecuados.

.. attribute:: DATABASES

   Un diccionario anidado que contiene la configuración de todas las bases de
   datos que se usarán en el sistema. Debe configurar por lo menos una base de
   datos predeterminada, también puede especificar cualquier número de bases de
   datos adicionales.

   Cuando esté en un ambiente de desarrollo podrá usar una base de datos SQLite
   que viene configurada de forma predefinida. En un ambiente de producción se
   recomienda usar otro backend de base de datos, como MySQL o PostgreSQL, que
   requerirán parámetros de conexión adicionales. Para mayor información
   visite: `<https://docs.djangoproject.com/en/2.1/ref/databases/>`_.

.. attribute:: STATIC_ROOT

   Ruta absoluta al directorio donde se almacenarán los archivos estáticos del
   proyecto.

   .. note::

      Debe asignar valor a `STATIC_ROOT` cuando despliegue en producción, de lo
      contrario ocurrirán errores al momento de procesar solicitudes de sus
      clientes.

.. attribute:: INSTALLED_APPS

   Lista que indica las aplicaciones que están habilitadas en el proyecto. Se
   incluye la `Interfaz de administración` de Django en el entorno de
   desarrollo.

   .. note::

      Se recomienda inhabilitar ``django.contrib.admin`` uando despliegue el sistema en producción.

.. attribute:: MEDIA_ROOT

   Ruta absoluta al directorio donde se almacenarán los archivos subidos por
   sus clientes.

.. attribute:: MEDIA_URL

   URL que maneja los archivos servidos desde `MEDIA_ROOT`. Debe terminar en
   un slash.

.. attribute:: CORS_ORIGIN_ALLOW_ALL

   Configuración del encabezado de las respuestas que le indican a los
   navegadores web que pueden realizar solicitudes desde origenes distintos a
   la ubicación del sistema. Es indispensable para que el API de GraphQL
   funcione.

   Si su valor es `True`, no se usará la lista blanca. Su valor está
   configurado para corresponder al valor de `DEBUG`.

.. attribute:: CORS_ORIGIN_WHITELIST

   Lista de nombres de host que tienen permitido hacer solicitudes HTTP desde
   un sitio cruzado.

   .. warning::

      Cuando despliegue el sistema en producción agregue los nombres de
      dominio, host o URL's desde las cuales se permitirá el acceso al API de
      GraphQL.
