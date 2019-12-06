"""
Entidades que participan en la gestión de sliders.

Para más información sobre los modelos de Django haga clic
`aquí <https://docs.djangoproject.com/en/2.1/topics/db/models/>`_.
"""

from django.db import models

from news.models import Post


class Slider(Post):
    """
    Agrupan imagenes y se utilizan en el sitio web de la VRCB.

    Hereda de :class:`news.models.Post`.
    """

    #: relación a :class:`news.models.Post` del cual hereda.
    post = models.OneToOneField(
        Post,
        on_delete=models.CASCADE,
        parent_link=True
    )
    #: posición del slider en el sitio web. Máximo 100 caracteres.
    position = models.CharField(max_length=100, default="NONE")
    #: descripción del slider. Máximo 144 caracteres.
    description = models.CharField(max_length=144)
    #: indica si el slider está activo. Valor predefinido `True`.
    active = models.BooleanField(default=True)
    #: fecha y hora de creación. Automático.
    created_at = models.DateTimeField(auto_now_add=True)
    #: fecha y hora de la última actualización. Automático.
    updated_at = models.DateTimeField(auto_now=True)
