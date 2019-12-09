"""
Entidades que participan en la gestión de noticias.

Para más información sobre los modelos de Django haga clic
`aquí <https://docs.djangoproject.com/en/2.1/topics/db/models/>`_.
"""

from datetime import date

from django.db import models
from django.template.defaultfilters import slugify


class Post(models.Model):
    """
    Modelo base para el contenido.

    Los demás tipos de contenido deben heredar de este modelo.
    """

    #: nombre del post. Máximo 64 caracteres.
    name = models.CharField(max_length=254)

    class Meta:
        verbose_name = "post"
        verbose_name_plural = "posts"

    def __str__(self):
        if hasattr(self, "news"):
            return self.name + "[News]"
        elif hasattr(self, "event"):
            return self.name + "[Event]"
        return self.name

class News(Post):
    """Noticias. Hereda desde :class:`Post`."""

    #: relación a :class:`Post` del cual hereda.
    post = models.OneToOneField(
        Post,
        on_delete=models.CASCADE,
        parent_link=True
    )
    #: nombre formateado de la noticia. Usado en las URL's web. Automático.
    slug = models.SlugField(
        max_length=64,
        db_index=True,
        unique=True,
        default="slug"
    )
    #: resumen corto de la noticia. Máximo 140 caracteres.
    abstract = models.CharField(max_length=140)
    #: contenido de la noticia.
    description = models.TextField()
    #: indica si la noticia debe ser mostrada. Valor predefinido `True`.
    active = models.BooleanField(default=True)
    #: fecha y hora de creación. Automático.
    created_at = models.DateTimeField(auto_now_add=True)
    #: fecha y hora de la última actualización. Automático.
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "noticia"
        verbose_name_plural = "noticias"

    def __str__(self):
        return self.slug

    def save(self, *args, **kwargs):
        """
        Sobrescritura del comportamiento al almacenamiento en base de datos.

        Se genera el slug de la noticia de forma automática en base al nombre.
        """
        name_addon = "-{date.month}-{date.year}".format(date=date.today())
        self.slug = slugify(self.name + name_addon)
        super().save(*args, **kwargs)

class Image(models.Model):
    """
    Imagen asociada a un elemento de contenido.

    Los contenido (noticias, eventos, etc.) pueden tener asociadas varias
    imagenes.
    """

    #: indica si la imágen es la destacada. Valor predefinido `False`.
    principal = models.BooleanField(default=False)
    #: archivo de la imágen.
    image_file = models.ImageField(upload_to="images/")
    #: fecha y hora de creación. Automático.
    created_at = models.DateTimeField(auto_now_add=True)
    #: fecha y hora de la última actualización. Automático.
    updated_at = models.DateTimeField(auto_now=True)
    #: contenido relacionado con la imágen.
    post = models.ForeignKey(
        Post,
        related_name="images",
        on_delete=models.CASCADE
    )

    class Meta:
        verbose_name = "imagen"
        verbose_name_plural = "imágenes"

    def __str__(self):
        return self.image_file.path
