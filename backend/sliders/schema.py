"""
Definición del esquema GraphQL para los sliders.

Para más información sobre los esquemas de Graphene Django haga clic
`aquí <http://docs.graphene-python.org/projects/django/en/latest/>`_.
"""

import graphene
from graphene_django import DjangoObjectType
from graphene_django.filter import DjangoFilterConnectionField
from graphql_jwt.decorators import login_required
from graphql_relay.node.node import from_global_id

from .models import Slider


# nodos y tipos
class SliderNode(DjangoObjectType):
    """
    Nodo de Graphql para los sliders.

    Implementa los siguientes filtros:
        :name: exacto, contiene
        :position: exacto
        :description: contiene
        :active: exact
    """

    class Meta:
        model = Slider
        filter_fields = {
            "name": ["exact", "icontains"],
            "position": ["exact"],
            "description": ["icontains"],
            "active": ["exact"]
        }
        interfaces = (graphene.relay.Node,)

# consultas
class SliderQuery():
    """Consultas de sliders."""

    #: consulta por un slider dado su identificador.
    slider = graphene.relay.Node.Field(SliderNode)
    #: consulta por todos los sliders.
    all_sliders = DjangoFilterConnectionField(SliderNode)

# mutaciones
class SliderMutationInput(graphene.InputObjectType):
    """Nodo de entrada para la creación y actualización de un slider."""

    #: nombre del slider. :attr:`sliders.models.Slider.name`
    name = graphene.String(required=True)
    #: posición en el sitio web. :attr:`sliders.models.Slider.position`
    position = graphene.String(required=True)
    #: descripción del slider. :attr:`sliders.models.Slider.description`
    description = graphene.String(required=True)
    #: indica si se debe mostrar. :attr:`sliders.models.Slider.active`
    active = graphene.Boolean(default_value=True)

class CreateSlider(graphene.relay.ClientIDMutation):
    """
    Registra un slider.

    Requiere autenticación mediante JWT. Ver :mod:`users.schema`.

    Entrada:
        :slider: :class:`SliderMutationInput`

    Retorna:
        :attr:`CreateSlider.new_slider`
    """

    #: slider recién creado. :class:`SliderNode`
    new_slider = graphene.Field(SliderNode)

    class Input:
        slider = graphene.Argument(SliderMutationInput, required=True)

    @classmethod
    @login_required
    def mutate_and_get_payload(cls, root, info, **input):
        """Registra el slider en la base de datos."""
        slider_data = input.get("slider")
        slider = Slider(
            name=slider_data.name,
            position=slider_data.position,
            description=slider_data.description,
            active=slider_data.active
        )
        slider.full_clean()
        slider.save()
        return cls(new_slider=slider)

class UpdateSlider(graphene.relay.ClientIDMutation):
    """
    Actualiza un slider.

    Requiere autenticación mediante JWT. Ver :mod:`users.schema`.

    Entrada:
        :id: identificador del slider que se va a actualizar.
        :slider: :class:`SliderMutationInput`

    Retorna:
        :attr:`UpdateSlider.updated_slider`
    """

    #: slider recién actualizado. :class:`SliderNode`
    updated_slider = graphene.Field(SliderNode)

    class Input:
        id = graphene.ID(required=True)
        slider = graphene.Argument(SliderMutationInput, required=True)

    @classmethod
    @login_required
    def mutate_and_get_payload(cls, root, info, **input):
        """Actualiza un slider en la base de datos."""
        relay_id = input.get("id")
        model_id = from_global_id(relay_id)[1]
        slider_instance = Slider.objects.get(id=model_id)
        if slider_instance:
            slider_data = input.get("slider")
            slider_instance.name = slider_data.name
            slider_instance.position = slider_data.position
            slider_instance.description = slider_data.description
            slider_instance.active = slider_data.active
            slider_instance.full_clean()
            slider_instance.save()
            return cls(updated_slider=slider_instance)
        raise Slider.DoesNotExist

class SliderMutation():
    """Mutaciones de sliders."""

    #: crea un slider. :class:`CreateSlider`
    create_slider = CreateSlider.Field()
    #: actualiza un slider. :class:`UpdateSlider`
    update_slider = UpdateSlider.Field()
