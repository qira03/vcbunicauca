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

from news.admin import ImagesInline

from .models import Slider


@admin.register(Slider)
class SliderAdmin(admin.ModelAdmin):
    """Interfaz administrativa de :class:`sliders.models.Slider`."""

    #: columnas de la lista de sliders.
    list_display = [
        "name",
        "position",
        "active"
    ]
    #: modelos asociados presentados como pila.
    inlines = [ImagesInline]
