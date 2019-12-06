"""
Definición del esquema principal GraphQL para el proyecto.

Para más información sobre los esquemas de Graphene Django haga clic
`aquí <http://docs.graphene-python.org/projects/django/en/latest/>`_.
"""

from django.dispatch import receiver
from graphene import ObjectType, Schema
from graphql_jwt import ObtainJSONWebToken, Refresh, Revoke, Verify
from graphql_jwt.refresh_token.signals import refresh_token_rotated

from events.schema import EventMutation, EventsQuery
from news.schema import NewsMutation, NewsQuery
from sliders.schema import SliderMutation, SliderQuery
from users.schema import UserMutation, UsersQuery


class Query(NewsQuery, EventsQuery, UsersQuery, SliderQuery, ObjectType):
    """
    Nodo que agrupa todas las consultas del proyecto.

    Consultas permitidas:
        :class:`news.schema.NewsQuery`
        :class:`events.schema.EventsQuery`
        :class:`users.schema.UsersQuery`
        :class:`sliders.schema.SliderQuery`
    """

class Mutation(
        NewsMutation,
        EventMutation,
        UserMutation,
        SliderMutation,
        ObjectType
    ):
    """
    Nodo que agrupa todas las mutaciones del proyecto.

    Mutaciones permitidas:
        :class:`news.schema.NewsMutation`
        :class:`events.schema.EventMutation`
        :class:`users.schema.UserMutation`
        :class:`sliders.schema.SliderMutation`

    También agrega las mutaciones que permiten la autenticación mediante JWT.
    `Más información <https://django-graphql-jwt.domake.io/en/stable/>`_.
    """

    #: autenticación por JWT.
    token_auth = ObtainJSONWebToken.Field()
    #: verifica la validez de un token.
    verify_token = Verify.Field()
    #: obtiene un nuevo token alargando la vida de la sesión.
    refresh_token = Refresh.Field()
    #: invalida un token.
    revoke_token = Revoke.Field()

@receiver(refresh_token_rotated)
def revoke_refresh_token(sender, refresh_token, **kwargs):
    """Invalida un token JWT."""
    refresh_token.revoke()

#: esquema principal para Graphene.
ROOT_SCHEMA = Schema(query=Query, mutation=Mutation)
