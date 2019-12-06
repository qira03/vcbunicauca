"""
Configuración de la interface administrativa de Django.

Para más información sobre la configuración de la interfaz de
administración de Django haga clic `aquí
<https://docs.djangoproject.com/en/2.1/ref/contrib/admin/>`_.

.. note::
    El sitio administrativo de Django sólo debe ser usado en el
    entorno de desarrollo, nunca en producción.
"""

from django.contrib import admin

from .models import Image, News


class ImagesInline(admin.StackedInline):
    """
    Interfaz administrativa para :class:`news.models.Image`.

    Las imagenes se mostrarán como una lista apilada, permitiendo su gestión de
    forma fácil desde la interfaz administrativa de :class:`news.models.Post`.
    """

    #: alias de :class:`news.models.Image`
    model = Image
    #: sólo una imágen adicional en el formulario.
    extra = 1

@admin.register(News)
class NewsAdmin(admin.ModelAdmin):
    """Interfaz administrativa de :class:`news.models.News`."""

    #: se excluye el slug ya que es automático.
    exclude = ["slug"]
    #: columnas de la lista de noticias.
    list_display = ("name", "active")
    #: modelos asociados presentados como pila.
    inlines = [ImagesInline]
