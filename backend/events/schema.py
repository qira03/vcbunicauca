"""
Definición del esquema GraphQL para los eventos.

Para más información sobre los esquemas de Graphene Django haga clic
`aquí <http://docs.graphene-python.org/projects/django/en/latest/>`_.
"""

import graphene
from django.forms import URLField
from graphene_django import DjangoObjectType
from graphene_django.filter import DjangoFilterConnectionField
from graphql_jwt.decorators import login_required
from graphql_relay.node.node import from_global_id

from .models import Category, Event, Organizer, RelatedLink, Venue


# nodos y Tipos
class CategoryNode(DjangoObjectType):
    """
    Nodo de Graphql para las categorías de eventos.

    Implementa los siguientes filtros:
        :name: exacto, contiene
        :slug: exacto
        :description: contiene
    """

    class Meta:
        model = Category
        filter_fields = {
            "name": ["exact", "icontains"],
            "slug": ["exact"],
            "description": ["icontains"]
        }
        interfaces = (graphene.relay.Node,)

class RelatedLinkNode(DjangoObjectType):
    """
    Nodo de Graphql para los enlaces relacionados de las categorías.

    Implementa los siguientes filtros:
        :name: exacto, contiene
    """

    class Meta:
        model = RelatedLink
        filter_fields = {"name": ["exact", "icontains"]}
        interfaces = (graphene.relay.Node,)

class VenueNode(DjangoObjectType):
    """
    Nodo de Graphql para los lugares de reunión de los eventos.

    Implementa los siguientes filtros:
        :name: exacto, contiene
        :address: exacto
        :city: exacto, contiene
        :state: exacto, contiene
    """

    class Meta:
        model = Venue
        filter_fields = {
            "name": ["exact", "icontains"],
            "address": ["exact"],
            "city": ["exact", "icontains"],
            "state": ["exact", "icontains"]
        }
        interfaces = (graphene.relay.Node,)

class OrganizerNode(DjangoObjectType):
    """
    Nodo de Graphql para los organizadores de los eventos.

    Implementa los siguientes filtros:
        :name: exacto, contiene
    """

    class Meta:
        model = Organizer
        filter_fields = {"name": ["exact", "icontains"]}
        interfaces = (graphene.relay.Node,)

class EventNode(DjangoObjectType):
    """
    Nodo de Graphql para los eventos.

    Implementa los siguientes filtros:
        :name: exacto, contiene
        :slug: exacto
        :start_datetime: exacto, mayor que, menor que
        :finish_datetime: exacto, mayor que, menor que
        :abstract: contiene
        :description: contiene
        :price: exacto, mayor que, menor que
        :active: exacto
        :created_at: exacto, mayor que, menor que
        :updated_at: exacto, mayor que, menor que
    """

    class Meta:
        model = Event
        filter_fields = {
            "name": ["exact", "icontains"],
            "slug": ["exact"],
            "start_datetime": ["exact", "gt", "lt"],
            "finish_datetime": ["exact", "gt", "lt"],
            "abstract": ["icontains"],
            "description": ["icontains"],
            "price": ["exact", "gt", "lt"],
            "active": ["exact"],
            "created_at": ["exact", "gt", "lt"],
            "updated_at": ["exact", "gt", "lt"]
        }
        interfaces = (graphene.relay.Node,)

# consultas
class EventsQuery():
    """Consultas de eventos."""

    #: consulta por una única categoría dado su identificador.
    category = graphene.relay.Node.Field(CategoryNode)
    #: consulta por un único enlace relacionado dado su identificador.
    related_link = graphene.relay.Node.Field(RelatedLinkNode)
    #: consulta por un único lugar de reunión dado su identificador.
    venue = graphene.relay.Node.Field(VenueNode)
    #: consulta por un único organizador de eventos dado su identificador.
    organizer = graphene.relay.Node.Field(OrganizerNode)
    #: consulta por un único evento dado su identificador.
    event = graphene.relay.Node.Field(EventNode)
    #: consulta por todas las categorías.
    all_categories = DjangoFilterConnectionField(CategoryNode)
    #: consulta por todos los enlaces relacionados.
    all_related_links = DjangoFilterConnectionField(RelatedLinkNode)
    #: consulta por todos los lugares de reunión de eventos.
    all_venues = DjangoFilterConnectionField(VenueNode)
    #: consulta por todos los organizadores de eventos.
    all_organizers = DjangoFilterConnectionField(OrganizerNode)
    #: consulta por todos los eventos.
    all_events = DjangoFilterConnectionField(EventNode)
    #: consulta por todos los eventos ordenados por fecha de creación.
    last_events = DjangoFilterConnectionField(EventNode)
    #: consulta por todos los eventos ordenados por fecha de inicio.
    recent_events = DjangoFilterConnectionField(EventNode)

    def resolve_last_events(self, info, **kwargs):
        """Devuelve los eventos en orden descendente por fecha de creación."""
        return Event.objects.all().order_by('-created_at')

    def resolve_recent_events(self, info, **kwargs):
        """Devuelve los eventos ordenados por fecha de inicio."""
        return Event.objects.all().order_by("start_datetime")

# mutaciones
class RelatedLinkMutationInput(graphene.InputObjectType):
    """Nodo de entrada para la creación y actualización de un enlace."""

    #: nombre del enlace relacionado. :attr:`events.models.RelatedLink.name`
    name = graphene.String(required=True)
    #: URL del enlace relacionado. :attr:`events.models.RelatedLink.link`
    link = graphene.String(required=True)

class CategoryCreateMutationInput(graphene.InputObjectType):
    """Nodo de entrada para la creación de una categoría de eventos."""

    #: nombre de la categoría. :attr:`events.models.Category.name`
    name = graphene.String(required=True)
    #: descripción de la categoría. :attr:`events.models.Category.description`
    description = graphene.String(required=True)
    #: nombre de la imágen representativa. :attr:`events.models.Category.image`
    image = graphene.String(required=True)

class CategoryUpdateMutationInput(graphene.InputObjectType):
    """
    Nodo de entrada para la actualización de una categoría de eventos.

    La diferencia con :class:`CategoryCreateMutationInput` radica en que la
    imágen es opcional en la actualización de la categoría.
    """

    #: nombre de la categoría. :attr:`events.models.Category.name`
    name = graphene.String(required=True)
    #: descripción de la categoría. :attr:`events.models.Category.description`
    description = graphene.String(required=True)
    #: nombre de la imágen representativa. :attr:`events.models.Category.image`
    image = graphene.String()

class VenueMutationInput(graphene.InputObjectType):
    """Nodo de entrada para la creación y actualización de lugares."""

    #: nombre del lugar. :attr:`events.models.Venue.name`
    name = graphene.String(required=True)
    #: dirección del lugar de reunión. :attr:`events.models.Venue.address`
    address = graphene.String(required=True)
    #: ciudad del lugar de reunión. :attr:`events.models.Venue.city`
    city = graphene.String(required=True, default_value="Popayán")
    #: departamento del lugar de reunión. :attr:`events.models.Venue.state`
    state = graphene.String(required=True, default_value="Cauca")
    #: teléfono de contacto. Opcional. :attr:`events.models.Venue.phone`
    phone = graphene.String(default_value="")
    #: sitio web. Opcional :attr:`events.models.Venue.website.`
    website = graphene.String(default_value="")
    #: coordenada x. :attr:`events.models.Venue.latitude`
    latitude = graphene.Float(required=True)
    #: coordenada y. :attr:`events.models.Venue.longitude`
    longitude = graphene.Float(required=True)

class OrganizerMutationInput(graphene.InputObjectType):
    """Nodo de entrada para la creación y actualización de organizadores."""

    #: nombre del organizador de eventos.
    name = graphene.String(required=True)
    #: teléfono de contacto del organizador. :attr:`events.models.Venue.phone`
    phone = graphene.String(default_value="")
    #: sitio web del organizador. :attr:`events.models.Venue.website`
    website = graphene.String(default_value="")
    #: email de contacto del organizador. :attr:`events.models.Venue.email`
    email = graphene.String(default_value="")

class EventMutationInput(graphene.InputObjectType):
    """Nodo de entrada para la creación y actualización de eventos."""

    #: nombre del evento. :attr:`events.models.Event.name`
    name = graphene.String(required=True)
    #: fecha y hora de inicio. :attr:`events.models.Event.start_datetime`
    start_datetime = graphene.DateTime(required=True)
    #: fecha y hora de cierre. :attr:`events.models.Event.finish_datetime`
    finish_datetime = graphene.DateTime(required=True)
    #: resumen del evento. :attr:`events.models.Event.abstract`
    abstract = graphene.String(required=True)
    #: descripción del evento. :attr:`events.models.Event.description`
    description = graphene.String(required=True)
    #: costo de entrada. :attr:`events.models.Event.price`
    price = graphene.Float(default_value=0)
    #: sitio web del evento. Opcional. :attr:`events.models.Event.website`
    website = graphene.String()
    #: indicador de cupo limitado. :attr:`events.models.Event.limited`
    limited = graphene.Boolean(default_value=False)
    #: indica si se debe mostrar. :attr:`events.models.Event.active`
    active = graphene.Boolean(default_value=True)
    #: lista de id's de categorías. :attr:`events.models.Event.categories`
    categories = graphene.List(graphene.ID, required=True)
    #: lista de id's de organizadores. :attr:`events.models.Event.organizers`
    organizers = graphene.List(graphene.ID, required=True)
    #: id del lugar de reunión. :attr:`events.models.Event.venue`
    venue = graphene.ID(required=True)

class CreateCategory(graphene.relay.ClientIDMutation):
    """
    Registra una categoría de eventos.

    Requiere autenticación mediante JWT. Ver :mod:`users.schema`.

    Entrada:
        :category: :class:`CategoryCreateMutationInput`

    Retorna:
        :attr:`CreateCategory.new_category`
    """

    #: categoría recién creada. :class:`CategoryNode`
    new_category = graphene.Field(CategoryNode)

    class Input:
        category = graphene.Argument(
            CategoryCreateMutationInput,
            required=True
        )

    @classmethod
    @login_required
    def mutate_and_get_payload(cls, root, info, **input):
        """Registra la categoría en la base de datos."""
        category_data = input.get("category")
        category = Category(
            name=category_data.name,
            description=category_data.description,
            image=info.context.FILES[category_data.image]
        )
        category.full_clean()
        category.save()
        return cls(new_category=category)

class UpdateCategory(graphene.relay.ClientIDMutation):
    """
    Actualiza la información de una categoría.

    Requiere autenticación mediante JWT. Ver :mod:`users.schema`.

    Entrada:
        :id: identificador de la categoría que se desea actualizar.
        :category: :class:`CategoryUpdateMutationInput`

    Retorna:
        :attr:`UpdateCategory.updated_category`
    """

    #: categoría recién actualizada. :class:`CategoryNode`.
    updated_category = graphene.Field(CategoryNode)

    class Input:
        id = graphene.ID(required=True)
        category = graphene.Argument(
            CategoryUpdateMutationInput,
            required=True
        )

    @classmethod
    @login_required
    def mutate_and_get_payload(cls, root, info, **input):
        """Actualiza una noticia en la base de datos."""
        relay_id = input.get("id")
        model_id = from_global_id(relay_id)[1]
        category_instance = Category.objects.get(id=model_id)
        if category_instance:
            category_data = input.get("category")
            category_instance.name = category_data.name
            category_instance.description = category_data.description
            if info.context.FILES and category_data.image:
                category_instance.image = info.context.FILES\
                    [category_data.image]
            category_instance.full_clean()
            category_instance.save()
            return cls(updated_category=category_instance)
        raise Category.DoesNotExist

class AddRelatedLinksToCategory(graphene.relay.ClientIDMutation):
    """
    Agrega enlaces relacionados a una categoría.

    Requiere autenticación mediante JWT. Ver :mod:`users.schema`

    Entrada:
        :id: identificador de la categoría a la cual se agregarán los enlaces.
        :related_links: lista de :class:`RelatedLinkMutationInput`

    Retorna:
        :attr:`AddRelatedLinksToCategory.category`
    """

    #: categoría a la cual se agregaron los enlaces. :class:`CategoryNode`
    category = graphene.Field(CategoryNode)

    class Input:
        id = graphene.Argument(graphene.ID, required=True)
        related_links = graphene.Argument(
            graphene.List(RelatedLinkMutationInput),
            required=True
        )

    @classmethod
    @login_required
    def mutate_and_get_payload(cls, root, info, **input):
        """Registra los enlaces relacionados en la base de datos."""
        category_relay_id = input.get("id")
        category_model_id = from_global_id(category_relay_id)[1]
        category_instance = Category.objects.get(id=category_model_id)
        if category_instance:
            related_links = input.get("related_links")
            if related_links:
                url_cleaner = URLField()
                for related_link in related_links:
                    link = RelatedLink(
                        name=related_link.name,
                        link=url_cleaner.clean(related_link.link),
                        category=category_instance
                    )
                    link.full_clean()
                    link.save()
                return cls(category=category_instance)
            else:
                raise IndexError("Debes enviar enlaces válidos.")
        raise Category.DoesNotExist

class DeleteRelatedLink(graphene.relay.ClientIDMutation):
    """
    Elimina un enlace relacionado.

    Requiere autenticación mediante JWT. Ver :mod:`users.schema`

    Entrada:
        :id: identificador del enlace relacionado que se va a eliminar.

    Retorna:
        :attr:`DeleteRelatedLink.success`
    """

    #: `True` si se eliminó el enlace, sino `False`
    success = graphene.Field(graphene.Boolean)

    class Input:
        id = graphene.ID(required=True)

    @classmethod
    @login_required
    def mutate_and_get_payload(cls, root, info, **input):
        """Elimina un enlace relacionado en la base de datos."""
        relay_id = input.get("id")
        model_id = from_global_id(relay_id)[1]
        related_link_instance = RelatedLink.objects.get(id=model_id)
        if related_link_instance:
            related_link_instance.delete()
            return cls(success=True)
        raise RelatedLink.DoesNotExist

class CreateVenue(graphene.relay.ClientIDMutation):
    """
    Registra un nuevo lugar de encuentro.

    Requiere autenticación mediante JWT. Ver :mod:`users.schema`

    Entrada:
        :venue: :class:`VenueMutationInput`

    Retorna:
        :attr:`CreateVenue.new_venue`
    """

    #: lugar de reunión recién creado. :class:`VenueNode`
    new_venue = graphene.Field(VenueNode)

    class Input:
        venue = graphene.Argument(VenueMutationInput, required=True)

    @classmethod
    @login_required
    def mutate_and_get_payload(cls, root, info, **input):
        """Registra el lugar en la base de datos."""
        venue_data = input.get("venue")
        url_cleaner = URLField(required=False)
        venue = Venue(
            name=venue_data.name,
            address=venue_data.address,
            city=venue_data.city,
            state=venue_data.state,
            phone=venue_data.phone,
            website=url_cleaner.clean(venue_data.website),
            latitude=venue_data.latitude,
            longitude=venue_data.longitude
        )
        venue.full_clean()
        venue.save()
        return cls(new_venue=venue)

class UpdateVenue(graphene.relay.ClientIDMutation):
    """
    Actualiza la información de un lugar de reunión de eventos.

    Requiere autenticación mediante JWT. Ver :mod:`users.schema`

    Entrada:
        :id: identificador del lugar que se actualizará.
        :venue: :class:`VenueMutationInput`

    Retorna:
        :attr:`UpdateVenue.updated_venue`
    """

    #: lugar de reunión recién actualizado. :class:`VenueNode`
    updated_venue = graphene.Field(VenueNode)

    class Input:
        id = graphene.ID(required=True)
        venue = graphene.Argument(VenueMutationInput, required=True)

    @classmethod
    @login_required
    def mutate_and_get_payload(cls, root, info, **input):
        """Actualiza un lugar en la base de datos."""
        relay_id = input.get("id")
        model_id = from_global_id(relay_id)[1]
        venue_instance = Venue.objects.get(id=model_id)
        if venue_instance:
            venue_data = input.get("venue")
            url_cleaner = URLField(required=False)
            venue_instance.name = venue_data.name
            venue_instance.address = venue_data.address
            venue_instance.city = venue_data.city
            venue_instance.state = venue_data.state
            venue_instance.phone = venue_data.phone
            venue_instance.website = url_cleaner.clean(venue_data.website)
            venue_instance.latitude = venue_data.latitude
            venue_instance.longitude = venue_data.longitude
            venue_instance.full_clean()
            venue_instance.save()
            return cls(updated_venue=venue_instance)
        raise Venue.DoesNotExist

class CreateOrganizer(graphene.relay.ClientIDMutation):
    """
    Registra un nuevo organizador de eventos.

    Requiere autenticación mediante JWT. Ver :mod:`users.schema`

    Entrada:
        :organizer: :class:`OrganizerMutationInput`

    Retorna:
        :attr:`CreateOrganizer.new_organizer`
    """

    #: organizador recién creado. :class:`OrganizerNode`
    new_organizer = graphene.Field(OrganizerNode)

    class Input:
        organizer = graphene.Argument(OrganizerMutationInput, required=True)

    @classmethod
    @login_required
    def mutate_and_get_payload(cls, root, info, **input):
        """Registra el organizador en la base de datos."""
        organizer_data = input.get("organizer")
        url_cleaner = URLField(required=False)
        organizer = Organizer(
            name=organizer_data.name,
            phone=organizer_data.phone,
            website=url_cleaner.clean(organizer_data.website),
            email=organizer_data.email
        )
        organizer.full_clean()
        organizer.save()
        return cls(new_organizer=organizer)

class UpdateOrganizer(graphene.relay.ClientIDMutation):
    """
    Actualiza la información de un organizador.

    Requiere autenticación mediante JWT. Ver :mod:`users.schema`

    Entrada:
        :id: identificador del organizador que se va a actualizar.
        :organizer: class:`OrganizerMutationInput`

    Retorna:
        :attr:`UpdateOrganizer.updated_organizer`
    """

    #: organizador recién actualizado. :class:`OrganizerNode`
    updated_organizer = graphene.Field(OrganizerNode)

    class Input:
        id = graphene.ID(required=True)
        organizer = graphene.Argument(OrganizerMutationInput, required=True)

    @classmethod
    @login_required
    def mutate_and_get_payload(cls, root, info, **input):
        """Actualiza un organizador en la base de datos."""
        relay_id = input.get("id")
        model_id = from_global_id(relay_id)[1]
        organizer_instance = Organizer.objects.get(id=model_id)
        if organizer_instance:
            organizer_data = input.get("organizer")
            url_cleaner = URLField(required=False)
            organizer_instance.name = organizer_data.name
            organizer_instance.phone = organizer_data.phone
            organizer_instance.website \
                = url_cleaner.clean(organizer_data.website)
            organizer_instance.email = organizer_data.email
            organizer_instance.full_clean()
            organizer_instance.save()
            return cls(updated_organizer=organizer_instance)
        raise Organizer.DoesNotExist

class CreateEvent(graphene.relay.ClientIDMutation):
    """
    Registra un nuevo evento y sus imágenes.

    Requiere autenticación mediante JWT. Ver :mod:`users.schema`

    Entrada:
        :event: :class:`EventMutationInput`

    Retorna:
        :attr:`CreateEvent.new_event`
    """

    #: evento recién creado. :class:`EventNode`
    new_event = graphene.Field(EventNode)

    class Input:
        event = graphene.Argument(EventMutationInput, required=True)

    @classmethod
    @login_required
    def mutate_and_get_payload(cls, root, info, **input):
        """Registra el evento en la base de datos."""
        # crear la instancia de Event
        event_data = input.get("event")
        url_cleaner = URLField(required=False)
        event = Event(
            name=event_data.name,
            start_datetime=event_data.start_datetime,
            finish_datetime=event_data.finish_datetime,
            abstract=event_data.abstract,
            description=event_data.description,
            price=event_data.price,
            website=url_cleaner.clean(event_data.website),
            limited=event_data.limited,
            active=event_data.active
        )
        # asignar el lugar de encuentro.
        venue_id = from_global_id(event_data.venue)[1]
        event.venue = Venue.objects.get(id=venue_id)
        event.full_clean()
        event.save()
        # recuperar y asignar las categorías
        if event_data.categories:
            for organizer_id in event_data.organizers:
                decoded_id = from_global_id(organizer_id)[1]
                event.organizers.add(Organizer.objects.get(id=decoded_id))
        else:
            # deshacer la transacción
            event.delete()
            raise ValueError("Events need at least one category")
        # recuperar y asignar los organizadores
        if event_data.organizers:
            for category_id in event_data.categories:
                decoded_id = from_global_id(category_id)[1]
                event.categories.add(Category.objects.get(id=decoded_id))
        else:
            # deshacer la transacción
            event.delete()
            raise ValueError("Events need at least one organizer")
        return cls(new_event=event)

class UpdateEvent(graphene.relay.ClientIDMutation):
    """
    Actualiza la información de un evento.

    Requiere autenticación mediante JWT. Ver :mod:`users:schema`

    Entrada:
        :id: identificador del evento que se va a actualizar.
        :event: :class:`EventMutationInput`

    Retorna:
        :attr:`UpdateEvent.updated_event`
    """

    #: event recién actualizado. :class:`EventNode`
    updated_event = graphene.Field(EventNode)

    class Input:
        id = graphene.ID(required=True)
        event = graphene.Argument(EventMutationInput, required=True)

    @classmethod
    def mutate_and_get_payload(cls, root, info, **input):
        """Actualiza un evento en la base de datos."""
        # recuperar la instancia de Event y asignar los nuevos valores
        relay_id = input.get("id")
        model_id = from_global_id(relay_id)[1]
        event_instance = Event.objects.get(id=model_id)
        if event_instance:
            event_data = input.get("event")
            url_cleaner = URLField(required=False)
            event_instance.name = event_data.name
            event_instance.start_datetime = event_data.start_datetime
            event_instance.finish_datetime = event_data.finish_datetime
            event_instance.abstract = event_data.abstract
            event_instance.description = event_data.description
            event_instance.price = event_data.price
            event_instance.website = url_cleaner.clean(event_data.website)
            event_instance.limited = event_data.limited
            event_instance.active = event_data.active
            # recuperar y re-asignar el lugar de encuentro
            venue_id = from_global_id(event_data.venue)[1]
            event_instance.venue = Venue.objects.get(id=venue_id)
            event_instance.full_clean()
            # re-asignar las categorías
            if event_data.categories:
                event_instance.categories.clear()
                for category_id in event_data.categories:
                    decoded_id = from_global_id(category_id)[1]
                    category = Category.objects.get(id=decoded_id)
                    event_instance.categories.add(category)
            else:
                raise ValueError("Events need at least one category")
            # re-asignar los organizadores
            if event_data.organizers:
                event_instance.organizers.clear()
                for organizer_id in event_data.organizers:
                    decoded_id = from_global_id(organizer_id)[1]
                    organizer = Organizer.objects.get(id=decoded_id)
                    event_instance.organizers.add(organizer)
            else:
                raise ValueError("Events need at least one organizer")
            event_instance.save()
            return cls(updated_event=event_instance)
        raise Event.DoesNotExist

class DeleteEvent(graphene.relay.ClientIDMutation):

    success = graphene.Field(graphene.Boolean)

    class Input:
        id = graphene.ID(required=True)

    @classmethod
    @login_required
    def mutate_and_get_payload(cls, root, info, **input):

        relay_id = input.get("id")
        model_id = from_global_id(relay_id)[1]
        event_instance = Event.objects.get(id=model_id)

        if event_instance:
            event_instance.delete()
            return cls(success=True)
        raise Event.DoesNotExist

class EventMutation():
    """Mutaciones de eventos."""

    #: crea una categoría de eventos. :class:`CreateCategory`
    create_category = CreateCategory.Field()
    #: crea un lugar de reunión. :class:`CreateVenue`
    create_venue = CreateVenue.Field()
    #: crea un organizador de eventos. :class:`CreateOrganizer`
    create_organizer = CreateOrganizer.Field()
    #: crea un evento. :class:`CreateEvent`
    create_event = CreateEvent.Field()
    #: actualiza una categoría de eventos. :class:`UpdateCategory`
    update_category = UpdateCategory.Field()
    #: actualiza un lugar de reunión. :class:`UpdateVenue`
    update_venue = UpdateVenue.Field()
    #: actualiza un organizador de eventos. :class:`UpdateOrganizer`
    update_organizer = UpdateOrganizer.Field()
    #: actualiza un evento. :class:`UpdateEvent`
    update_event = UpdateEvent.Field()
    #: agrega enlaces a una categoría. :class:`AddRelatedLinksToCategory`
    add_related_links_to_category = AddRelatedLinksToCategory.Field()
    #: elimina enlaces de una categoría. :class:`DeleteRelatedLink`
    delete_related_link = DeleteRelatedLink.Field()

    delete_event = DeleteEvent.Field()
