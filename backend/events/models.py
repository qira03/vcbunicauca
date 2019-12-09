"""
Entidades que participan en la gestión de eventos.

Para más información sobre los modelos de Django haga clic
`aquí <https://docs.djangoproject.com/en/2.1/topics/db/models/>`_.
"""

from datetime import date

from django.core.exceptions import ValidationError
from django.db import models
from django.template.defaultfilters import slugify

from news.models import Post


class Category(models.Model):
    """Las categorías agrupan los eventos para facilitar su búsqueda."""

    #: nombre de la categoría. Máximo 64 caracteres.
    name = models.CharField(max_length=64)
    #: nombre formateado de la categoría. Usado en las URL's web. Automático.
    slug = models.SlugField(
        max_length=90,
        db_index=True,
        unique=True,
        default="slug"
    )
    #: descripción de la categoría. Máximo 140 caracteres.
    description = models.CharField(max_length=6000)
    #: imágen representativa de la categoría.
    image = models.ImageField(upload_to="images/")
    #: fecha y hora de creación. Automático.
    created_at = models.DateTimeField(auto_now_add=True)
    #: fecha y hora de la última actualización. Automático.
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "categoría"
        verbose_name_plural = "categorías"

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        """
        Sobrescribe el comportamiento al almacenamiento en base de datos.

        Se genera el slug de la categoría de forma automática en base al
        nombre.
        """
        name_addon = "-{date.month}-{date.year}".format(date=date.today())
        self.slug = slugify(self.name + name_addon)
        super().save(*args, **kwargs)

class RelatedLink(models.Model):
    """Enlaces relacionados a sitios de interés."""

    #: nombre del enlace relacionado. Máximo 120 caracteres.
    name = models.CharField(max_length=254)
    #: URL del enlace relacionado. Máximo 250 caracteres.
    link = models.URLField(max_length=250)
    #: fecha y hora de creación. Automático.
    created_at = models.DateTimeField(auto_now_add=True)
    #: fecha y hora de la última actualización. Automático.
    updated_at = models.DateTimeField(auto_now=True)
    #: categoría a la que pertenece el enlace relacionado.
    category = models.ForeignKey(
        Category,
        related_name="related_links",
        on_delete=models.CASCADE
    )

    class Meta:
        verbose_name = "Enlace de interés"
        verbose_name_plural = "Enlaces de interés"

    def __str__(self):
        return self.path

class Venue(models.Model):
    """Lugares de reunión donde se realizan los eventos."""

    #: nombre del lugar. Máximo 96 caracteres.
    name = models.CharField(max_length=96)
    #: dirección del lugar. Máximo 64 caracteres.
    address = models.CharField(max_length=64)
    #: ciudad del lugar. Valor predefinido "Popayán". Máximo 32 caracteres.
    city = models.CharField(max_length=32, default="Popayán")
    #: departamento. Valor predefinido "Cauca". Máximo 32 caracteres.
    state = models.CharField(max_length=32, default="Cauca")
    #: teléfono de contacto. Opcional. Máximo 18 caracteres.
    phone = models.CharField(max_length=18, null=True, blank=True)
    #: sitio web del lugar. Opcional.
    website = models.URLField(null=True, blank=True)
    #: coordenada x del lugar.
    latitude = models.FloatField()
    #: coordenada y del lugar.
    longitude = models.FloatField()
    #: fecha y hora de creación. Automático.
    created_at = models.DateTimeField(auto_now_add=True)
    #: fecha y hora de la última actualización. Automático.
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "lugar"
        verbose_name_plural = "lugares"

    def __str__(self):
        return self.name

class Organizer(models.Model):
    """Organizadores de eventos."""

    #: nombre del organizador. Máximo 80 caracteres.
    name = models.CharField(max_length=80)
    #: teléfono de contacto. Opcional. Máximo 18 caracteres.
    phone = models.CharField(max_length=18, null=True, blank=True)
    #: sitio web del organizador. Opcional.
    website = models.URLField(null=True, blank=True)
    #: email de contacto. Opcional.
    email = models.EmailField(null=True, blank=True)
    #: fecha y hora de creación. Automático.
    created_at = models.DateTimeField(auto_now_add=True)
    #: fecha y hora de la última actualización. Automático.
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "organizador"
        verbose_name_plural = "organizadores"

    def __str__(self):
        return self.name

class Event(Post):
    """Eventos culturales y sociales. Hereda de :class:`news.models.Post`."""

    #: relación a :class:`news.models.Post` del cual hereda.
    post = models.OneToOneField(
        Post,
        on_delete=models.CASCADE,
        parent_link=True
    )
    #: nombre formateado del evento. Usado en las URL's web. Automático.
    slug = models.SlugField(
        max_length=128,
        db_index=True,
        unique=True,
        default="slug"
    )
    #: fecha y hora de inicio del evento.
    start_datetime = models.DateTimeField()
    #: fecha y hora de cierre del evento.
    finish_datetime = models.DateTimeField()
    #: resumen corto del evento. Opcional. Máximo 140 caracteres.
    abstract = models.CharField(max_length=6000, null=True, blank=True)
    #: descripción completa del evento.
    description = models.TextField()
    #: costo de entrada al evento. Valor predefinido 0 (evento gratuito).
    price = models.FloatField(default=0)
    #: sitio web del evento. Opcional.
    website = models.URLField(null=True, blank=True)
    #: indica si el evento tiene cupo limitado. Valor predefinido `False`.
    limited = models.BooleanField(default=False)
    #: indica si el evento debe ser mostrado. Valor predefinido `True`.
    active = models.BooleanField(default=True)
    #: fecha y hora de creación. Automático.
    created_at = models.DateTimeField(auto_now_add=True)
    #: fecha y hora de la última actualización. Automático.
    updated_at = models.DateTimeField(auto_now=True)
    #: listado de categorías a las que pertenece el evento.
    categories = models.ManyToManyField(Category, related_name="events")
    #: listado de organizadores del evento.
    organizers = models.ManyToManyField(Organizer, related_name="events")
    #: lugar de realización del evento.
    venue = models.ForeignKey(
        Venue,
        related_name="events",
        on_delete=models.DO_NOTHING
    )

    class Meta:
        verbose_name = "evento"
        verbose_name_plural = "eventos"

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        """
        Sobrescritura del comportamiento al almacenamiento en base de datos.

        Valida que la fecha de cierre del evento no puede ser anterior a la de
        inicio y genera el slug del evento de forma automática en base al nombre.
        """
        if self.finish_datetime <= self.start_datetime:
            raise ValidationError({
                "finish_datetime": ValidationError(
                    "La fecha de finalización debe ser posterior a la fecha "\
                        "deinicio.",
                    code="invalid"
                )
            })
        name_addon = "-{date.month}-{date.year}".format(date=date.today())
        self.slug = slugify(self.name + name_addon)
        super().save(*args, **kwargs)
