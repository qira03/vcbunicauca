"""
Definición del esquema GraphQL para las noticias.

Para más información sobre los esquemas de Graphene Django haga clic
`aquí <http://docs.graphene-python.org/projects/django/en/latest/>`_.
"""

import graphene
from graphene_django import DjangoObjectType
from graphene_django.filter import DjangoFilterConnectionField
from graphql_jwt.decorators import login_required
from graphql_relay.node.node import from_global_id

from .models import Image, News, Post


# Nodos y Tipos
class PostNode(DjangoObjectType):
    """
    Nodo de Graphql para los posts.

    La definición de este nodo permite a los demás tipos contenido acceder a
    los atributos de su clase general.
    """

    class Meta:
        model = Post
        interfaces = (graphene.relay.Node,)

class NewsNode(DjangoObjectType):
    """
    Nodo de Graphql para las noticias.

    Implementa los siguientes filtros:
        :name: exacto, contiene
        :slug: exacto
        :abstract: contiene
        :description: contiene
        :active: exacto
        :created_at: exacto, mayor que, menor que
        :updated_at: exacto, mayor que, menor que
    """

    class Meta:
        model = News
        filter_fields = {
            "name": ["exact", "icontains"],
            "slug": ["exact"],
            "abstract": ["icontains"],
            "description": ["icontains"],
            "active": ["exact"],
            "created_at": ["exact", "gt", "lt"],
            "updated_at": ["exact", "gt", "lt"]
        }
        interfaces = (graphene.relay.Node,)

class ImageNode(DjangoObjectType):
    """
    Nodo de Graphql para las imagenes asociadas al contenido.

    Implementa los siguientes filtros:
        :principal: exacto
    """

    class Meta:
        model = Image
        filter_fields = ["principal"]
        interfaces = (graphene.relay.Node,)

# consultas
class NewsQuery():
    """Consultas de noticias."""

    #: consulta por una única noticia dado su identificador.
    news = graphene.relay.Node.Field(NewsNode)
    #: consulta por todas las noticias.
    all_news = DjangoFilterConnectionField(NewsNode)
    #: consulta por todas las noticias ordenadas por fecha de creación.
    last_news = DjangoFilterConnectionField(NewsNode)

    def resolve_last_news(self, info, **kwargs):
        """Devuelve las últimas noticias en orden descendente por fecha."""
        return News.objects.all().order_by('-created_at')

# mutaciones
class ImageCreateMutationInput(graphene.InputObjectType):
    """Nodo de entrada para la creación de imagenes asociadas a contenido."""

    #: nombre de la imágen. :attr:`news.models.Image.image_file`
    image_file = graphene.String(required=True)
    #: indica si es la imágen destacada. :attr:`news.models.Image.principal`
    principal = graphene.Boolean(default_value=False)

class ImageUpdateMutationInput(graphene.InputObjectType):
    """
    Nodo de entrada para la actualización de imagenes.

    La diferencia con :class:`ImageCreateMutationInput` radica en que la imágen
    es opcional, permitiendo actualizar solo el valor de `principal`.
    """

    #: nombre de la imágen. :attr:`news.models.Image.image_file`
    image_file = graphene.String()
    #: indica si es la imágen destacada. :attr:`news.models.Image_principal`
    principal = graphene.Boolean(default_value=False)

class NewsMutationInput(graphene.InputObjectType):
    """Nodo de entrada para la creación y actualización de noticias."""

    #: nombre de la noticia. :attr:`news.models.News.name`
    name = graphene.String(required=True)
    #: resumen de la noticia. :attr:`news.models.News.abstract`
    abstract = graphene.String(required=True)
    #: contenido de la noticia. :attr:`news.models.News.description`
    description = graphene.String(required=True)
    #: indica si se debe mostrar. :attr:`news.models.News.active`
    active = graphene.Boolean(default_value=True)

class CreateNews(graphene.relay.ClientIDMutation):
    """Registra una nueva noticia.

    Requiere autenticación mediante JWT. Ver :mod:`users.schema`.

    Entrada:
        :news: :class:`NewsMutationInput`

    Retorna:
        :attr:`CreateNews.new_news`
    """

    #: noticia recién creada. :class:`NewsNode`
    new_news = graphene.Field(NewsNode)

    class Input:
        news = graphene.Argument(NewsMutationInput, required=True)

    @classmethod
    @login_required
    def mutate_and_get_payload(cls, root, info, **input):
        """Registra la noticia en la base de datos."""
        news_data = input.get("news")
        news = News(
            name=news_data.name,
            abstract=news_data.abstract,
            description=news_data.description,
            active=news_data.active
        )
        news.full_clean()
        news.save()
        return cls(new_news=news)

class UpdateNews(graphene.relay.ClientIDMutation):
    """Actualiza la información de una noticia.

    Requiere autenticación mediante JWT. Ver :mod:`users.schema`.

    Entrada:
        :id: identificador de la noticia que se va a actualizar.
        :news: :class:`NewsMutationInput`

    Retorna:
        :attr:`UpdateNews.updated_news`
    """

    #: noticia recién actualizada. :class:`NewsNode`
    updated_news = graphene.Field(NewsNode)

    class Input:
        id = graphene.ID(required=True)
        news = graphene.Argument(NewsMutationInput, required=True)

    @classmethod
    @login_required
    def mutate_and_get_payload(cls, root, info, **input):
        """Actualiza una noticia en la base de datos."""
        relay_id = input.get("id")
        model_id = from_global_id(relay_id)[1]
        news_instance = News.objects.get(id=model_id)
        if news_instance:
            news_data = input.get("news")
            news_instance.name = news_data.name
            news_instance.abstract = news_data.abstract
            news_instance.description = news_data.description
            news_instance.active = news_data.active
            news_instance.full_clean()
            news_instance.save()
            return cls(updated_news=news_instance)
        raise News.DoesNotExist

class AddImagesToPost(graphene.relay.ClientIDMutation):
    """
    Agrega imagenes a un post.

    Requiere autenticación mediante JWT. Ver :mod:`users.schema`.

    Entrada:
        :id: identificador del post al cual se agregarán las imagenes.
        :images: lista de :class:`ImageCreateMutationInput`

    Retorna:
        :attr:`AddImagesToPost.post`
    """

    #: post al cual se agregaron las imagenes. :class:`PostNode`
    post = graphene.Field(PostNode)

    class Input:
        id = graphene.Argument(graphene.ID, required=True)
        images = graphene.Argument(
            graphene.List(ImageCreateMutationInput),
            required=True
        )

    @classmethod
    @login_required
    def mutate_and_get_payload(cls, root, info, **input):
        """Registra la  nueva imagen en la base de datos."""
        post_relay_id = input.get("id")
        post_model_id = from_global_id(post_relay_id)[1]
        post_instance = Post.objects.get(id=post_model_id)
        if post_instance:
            images = input.get("images")
            if info.context.FILES and images:
                for image_data in images:
                    image = Image(
                        post=post_instance,
                        principal=image_data.principal,
                        image_file=info.context.FILES[image_data.image_file]
                    )
                    image.full_clean()
                    image.save()
                return cls(post=post_instance)
            else:
                raise IndexError("Debes enviar imágenes válidas.")
        raise Post.DoesNotExist

class UpdateImage(graphene.relay.ClientIDMutation):
    """Actualiza la información de una imagen.

    Requiere autenticación mediante JWT. Ver :mod:`users.schema`

    Entrada:
        :id: identificador de la imágen que se va a actualizar.
        :image: :class:`ImageUpdateMutationInput`

    Retorna:
        :attr:`UpdateImage.updated_image`
    """

    #: imágen recién actualizada. :class:`ImageNode`
    updated_image = graphene.Field(ImageNode)

    class Input:
        id = graphene.ID(required=True)
        image = graphene.Argument(ImageUpdateMutationInput, required=True)

    @classmethod
    @login_required
    def mutate_and_get_payload(cls, root, info, **input):
        """Actualiza una imagen en la base de datos."""
        relay_id = input.get("id")
        model_id = from_global_id(relay_id)[1]
        image_instance = Image.objects.get(id=model_id)
        if image_instance:
            image_data = input.get("image")
            image_instance.principal = image_data.principal
            if info.context.FILES:
                image_instance.image_file = info.context.FILES[image_data.image_file]
            image_instance.full_clean()
            image_instance.save()
            return cls(updated_image=image_instance)
        raise Image.DoesNotExist

class DeleteImage(graphene.relay.ClientIDMutation):
    """Elimina una imagen.

    Requiere autenticación mediante JWT. Ver :mod:`users.schema`.

    Entrada:
        :id: identificador de la imágen que se va a eliminar.

    Retorna:
        :attr:`DeleteImage.success`
    """

    #: `True` si se eliminó la imágen, sino `False`.
    success = graphene.Field(graphene.Boolean)

    class Input:
        id = graphene.ID(required=True)

    @classmethod
    @login_required
    def mutate_and_get_payload(cls, root, info, **input):
        """Elimina una imagen en la base de datos."""
        relay_id = input.get("id")
        model_id = from_global_id(relay_id)[1]
        image_instance = Image.objects.get(id=model_id)
        if image_instance:
            image_instance.delete()
            return cls(success=True)
        raise Image.DoesNotExist

class DeleteNews(graphene.relay.ClientIDMutation):

    success = graphene.Field(graphene.Boolean)

    class Input:
        id = graphene.ID(required=True)

    @classmethod
    @login_required
    def mutate_and_get_payload(cls, root, info, **input):

        relay_id = input.get("id")
        model_id = from_global_id(relay_id)[1]
        news_instance = News.objects.get(id=model_id)

        if news_instance:
            news_instance.delete()
            return cls(success=True)
        raise News.DoesNotExist

class NewsMutation():
    """Mutaciones de noticias e imágenes."""

    #: crea una noticia. :class:`CreateNews`
    create_news = CreateNews.Field()
    #: actualiza una noticia. :class:`UpdateNews`
    update_news = UpdateNews.Field()
    #: agrega imagenes a un post. :class:`AddImagesToPost`
    add_images_to_post = AddImagesToPost.Field()
    #: actualiza una imágen de un post. :class:`UpdateImage`
    update_image = UpdateImage.Field()
    #: elimina una imágen de un post. :class:`DeleteImage`
    delete_image = DeleteImage.Field()

    delete_news= DeleteNews.Field()
