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

from .models import Category, Event, Organizer, RelatedLink, Venue


class RelatedLinkInline(admin.StackedInline):
    """
    Interfaz administrativa para :class:`events.models.RelatedLink`.

    Los enlaces relacionados se mostrarán como una lista apilada, permitiendo
    su gestión de forma fácil desde la interfaz administrativa de :class:`events.models.Category`.
    """

    #: alias de :class:`events.models.RelatedLink`
    model = RelatedLink
    #: sólo un enlace relacionado adicional en el formulario.
    extra = 1

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    """Interfaz administrativa de :class:`events.models.Category`."""

    #: se excluye el slug ya que es automático.
    exclude = ["slug"]
    #: columnas de la lista de categorías.
    list_display = ("name", "image")
    #: modelos asociados presentados como pila.
    inlines = [RelatedLinkInline]

@admin.register(Venue)
class VenueAdmin(admin.ModelAdmin):
    """Interfaz administrativa de :class:`events.models.Venue`."""

    #: columnas de la lista de lugares de reunión.
    list_display = (
        "name",
        "address",
        "city",
        "state",
        "latitude",
        "longitude"
    )

@admin.register(Organizer)
class OrganizerAdmin(admin.ModelAdmin):
    """Interfaz administrativa de :class:`events.models.Organizer`."""

    #: columnas de la lista de organizadores.
    list_display = ("name", "email")

@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    """Interfaz administrativa de :class:`events.models.Event`."""

    #: se excluye el slug ya que es automático.
    exclude = ["slug"]
    #: columnas de la lista de eventos.
    list_display = [
        "name",
        "start_datetime",
        "finish_datetime",
        "price",
        "venue",
        "active"
    ]
    #: modelos asociados presentados como pila.
    inlines = [ImagesInline]
