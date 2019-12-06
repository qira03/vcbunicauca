"""
Definición del esquema GraphQL para los usuarios.

Para más información sobre los esquemas de Graphene Django haga clic
`aquí <http://docs.graphene-python.org/projects/django/en/latest/>`_.
"""

import graphene
from django.contrib.auth.models import User
from graphene_django import DjangoObjectType
from graphene_django.filter import DjangoFilterConnectionField
from graphql_jwt.decorators import login_required
from graphql_relay.node.node import from_global_id


# nodos y Tipos
class UserNode(DjangoObjectType):
    """
    Nodo de Graphql para la consulta de usuarios.

    Implementa los siguientes filtros:
        :username: exacto
        :email: exacto
        :first_name: exacto
        :last_name: exacto

    Atributos excluídos:
        :password:
    """

    class Meta:
        model = User
        filter_fields = ["username", "email", "first_name", "last_name"]
        exclude_fields = ('password',)
        interfaces = (graphene.relay.Node,)

    @classmethod
    @login_required
    def get_node(cls, info, id):
        """
        Sobrescribe el método agregando autenticación.

        Requiere autenticación mediante JWT.

        Entrada:
            :id: identificador del usuario.

        Retorna:
            :User:
        """
        try:
            return cls._meta.model.objects.get(pk=id)
        except cls._meta.model.DoesNotExist:
            return None

# consultas
class UsersQuery():
    """Consultas de usuarios."""

    #: consulta por un usuario dado su identificador.
    user = graphene.relay.Node.Field(UserNode)
    #: consulta por todos los usuarios.
    all_users = DjangoFilterConnectionField(UserNode)

    @login_required
    def resolve_all_users(self, info, **kwargs):
        """
        Sobrescribe el método agregando autenticación.

        Requiere autenticación mediante JWT.

        Entrada:
            filtros soportados por :class:`UserNode`.

        Retorna:
            Lista de :User:
        """
        return User.objects.all()

# mutaciones
class UserCreateMutationInput(graphene.InputObjectType):
    """Nodo de entrada para la creación de un usuario."""

    #: nombre de usuario.
    username = graphene.String(required=True)
    #: contraseña del usuario.
    password = graphene.String(required=True)
    #: email del usuario.
    email = graphene.String(required=True)
    #: nombres reales del usuario.
    first_name = graphene.String(default_value="")
    #: apellidos reales del usuario.
    last_name = graphene.String(default_value="")

class UserUpdateMutationInput(graphene.InputObjectType):
    """
    Nodo de entrada para la actualización de un usuario.

    El nombre de usuario y la contraseña no es modificables.
    """

    #: email del usuario.
    email = graphene.String(required=True)
    #: nombres reales del usurio.
    first_name = graphene.String(required=True)
    #: apellidos reales del usuario.
    last_name = graphene.String(required=True)
    #: indica si se habilida o no el usuario en el sistema.
    active = graphene.Boolean(default_value=True)

class CreateUser(graphene.relay.ClientIDMutation):
    """
    Registra un usuario en el sistema.

    Requiere autenticación mediante JWT.

    Entrada:
        :user: :class:`UserCreateMutationInput`

    Retorna:
        :attr:`CreateUser.new_user`
    """

    #: usuario recién creado. :class:`UserNode`
    new_user = graphene.Field(UserNode)

    class Input:
        user = graphene.Argument(UserCreateMutationInput, required=True)

    @classmethod
    @login_required
    def mutate_and_get_payload(cls, root, info, **input):
        """Registra un usuario en la base de datos."""
        user_data = input.get("user")
        user = User.objects.create_user(
            username=user_data.username,
            password=user_data.password,
            email=user_data.email,
            first_name=user_data.first_name,
            last_name=user_data.last_name
        )
        user.full_clean()
        user.save()
        return cls(new_user=user)

class UpdateUser(graphene.relay.ClientIDMutation):
    """
    Actualiza un usuario del sistema.

    Requiere autenticación mediante JWT.

    Entrada:
        :id: identificador del usuario que se va a actualizar.
        :user: :class:`UserUpdateMutationInput`

    Retorna:
        :attr:`UpdateUser.updated_user`
    """

    #: usuario recién actualizado. :class:`UserNode`
    updated_user = graphene.Field(UserNode)

    class Input:
        id = graphene.ID(required=True)
        user = graphene.Argument(UserUpdateMutationInput, required=True)

    @classmethod
    @login_required
    def mutate_and_get_payload(cls, root, info, **input):
        """Actualiza un usuario en la base de datos."""
        user_data = input.get("user")
        relay_id = input.get("id")
        user_id = from_global_id(relay_id)[1]
        user = User.objects.get(id=user_id)
        user.email = user_data.email
        user.first_name = user_data.first_name
        user.last_name = user_data.last_name
        user.is_active = user_data.active
        user.full_clean()
        user.save()
        return cls(updated_user=user)

class UpdateUserPassword(graphene.relay.ClientIDMutation):
    """
    Actualiza la contraseña de un usuario.

    Requiere autenticación mediante JWT.

    Entrada:
        :id: identificador del usuario al que se va a actualizar.
        :password: nueva contraseña.

    Retorna:
        :attr:`UpdateUserPassword.updated_user`
    """

    #: usuario recién actualizado. :class:`UserNode`
    updated_user = graphene.Field(UserNode)

    class Input:
        id = graphene.ID(required=True)
        password = graphene.String(required=True)

    @classmethod
    @login_required
    def mutate_and_get_payload(cls, root, info, **input):
        """Actualiza la contraseña de un usuario en la base de datos."""
        new_password = input.get("password")
        relay_id = input.get("id")
        user_id = from_global_id(relay_id)[1]
        user = User.objects.get(id=user_id)
        user.set_password(new_password)
        user.full_clean()
        user.save()
        return cls(updated_user=user)

class UserMutation():
    """Mutaciones de usuarios."""

    create_user = CreateUser.Field()
    update_user = UpdateUser.Field()
    update_user_password = UpdateUserPassword.Field()
