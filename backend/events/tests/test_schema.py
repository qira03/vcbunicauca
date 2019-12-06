"""Casos de prueba para el esquema GraphQL de eventos."""

import tempfile
from collections import OrderedDict
from datetime import datetime

import pytz
from django.contrib.auth import get_user_model
from django.test import TestCase
from graphene.test import Client
from graphql_jwt.testcases import JSONWebTokenTestCase

from events.models import Category, Event, Organizer, RelatedLink, Venue
from events.tests.test_model import TestSetup as EventTestSetup
from unicauca_vrcb.schema import ROOT_SCHEMA


class TestSetup():
    @staticmethod
    def setup():
        EventTestSetup.setup()

class CategoryQueriesTestCase(TestCase):

    graphql_client = Client(ROOT_SCHEMA)
    test_case_schema = {
        "category_1": {
            "name": "Categoría 1",
            "description": "Descripción categoría 1"
        },
        "category_2": {
            "name": "Categoría 2",
            "description": "Descripción categoría 2"
        }
    }

    def setUp(self):
        """Configuración del caso de prueba."""
        TestSetup.setup()
        category_1 = Category.objects.get(id=1)
        category_2 = Category.objects.get(id=2)
        self.test_case_schema["category_1"]["image"] = category_1.image.name
        self.test_case_schema["category_2"]["image"] = category_2.image.name

    def test_all_category(self):
        query_string = """
            query{
                allCategories{
                    edges{
                        node{
                            name
                            description
                            image
                        }
                    }
                }
            }
        """
        query_result = self.graphql_client.execute(query_string)
        expected_result = {
            "data": OrderedDict({
                "allCategories": OrderedDict({
                    "edges": [
                        OrderedDict({
                            "node": OrderedDict(
                                self.test_case_schema["category_1"]
                            )
                        }),
                        OrderedDict({
                            "node": OrderedDict(
                                self.test_case_schema["category_2"]
                            )
                        })
                    ]
                })
            })
        }
        self.assertEqual(query_result, expected_result)

    def test_single_category(self):
        query_string = """
            query{
                category(id: "Q2F0ZWdvcnlOb2RlOjE="){
                    name
                    description
                    image
                }
            }
        """
        query_result = self.graphql_client.execute(query_string)
        expected_result = {
            "data": OrderedDict({
                "category": OrderedDict(self.test_case_schema["category_1"])
            })
        }
        self.assertEqual(query_result, expected_result)

class RelatedLinkQueriesTestCase(TestCase):

    graphql_client = Client(ROOT_SCHEMA)
    test_case_schema = {
        "related_link_1": {
            "name": "Link 1",
            "link": "www.link1.com"
        },
        "related_link_2": {
            "name": "Link 2",
            "link": "www.link2.com"
        }
    }

    def setUp(self):
        """Configuración del caso de prueba."""
        TestSetup.setup()

    def test_all_related_links(self):
        query_string = """
            query{
                allRelatedLinks{
                    edges{
                        node{
                            name
                            link
                        }
                    }
                }
            }
        """
        query_result = self.graphql_client.execute(query_string)
        expected_result = {
            "data": OrderedDict({
                "allRelatedLinks": OrderedDict({
                    "edges": [
                        OrderedDict({
                            "node": OrderedDict(
                                self.test_case_schema["related_link_1"]
                            )
                        }),
                        OrderedDict({
                            "node": OrderedDict(
                                self.test_case_schema["related_link_2"]
                            )
                        })
                    ]
                })
            })
        }
        self.assertEqual(query_result, expected_result)

    def test_single_related_link(self):
        query_string = """
            query{
                relatedLink(id: "UmVsYXRlZExpbmtOb2RlOjE="){
                    name
                    link
                }
            }
        """
        query_result = self.graphql_client.execute(query_string)
        expected_result = {
            "data": OrderedDict({
                "relatedLink": OrderedDict(self.test_case_schema["related_link_1"])
            })
        }
        self.assertEqual(query_result, expected_result)

class VenueQueriesTestCase(TestCase):

    graphql_client = Client(ROOT_SCHEMA)
    test_case_schema = {
        "venue_1": {
            "name": "Lugar 1",
            "address": "Calle A 11",
            "city": "Popayán",
            "state": "Cauca",
            "phone": "3202962997",
            "website": "https://www.venue1.com",
            "latitude": 1.100,
            "longitude": 2.200
        },
        "venue_2": {
            "name": "Lugar 2",
            "address": "Valle ABC 123",
            "city": "Popayán",
            "state": "Cauca",
            "phone": None,
            "website": None,
            "latitude": 3.300,
            "longitude": 4.400
        }
    }

    def setUp(self):
        """Configuración del caso de prueba."""
        TestSetup.setup()

    def test_all_venues(self):
        query_string = """
            query{
                allVenues{
                    edges{
                        node{
                            name
                            address
                            city
                            state
                            phone
                            website
                            latitude
                            longitude
                        }
                    }
                }
            }
        """
        query_result = self.graphql_client.execute(query_string)
        expected_result = {
            "data": OrderedDict({
                "allVenues": OrderedDict({
                    "edges": [
                        OrderedDict({
                            "node": OrderedDict(
                                self.test_case_schema["venue_1"]
                            )
                        }),
                        OrderedDict({
                            "node": OrderedDict(
                                self.test_case_schema["venue_2"]
                            )
                        })
                    ]
                })
            })
        }
        self.assertEqual(query_result, expected_result)

    def test_single_venue(self):
        query_string = """
            query{
                venue(id: "VmVudWVOb2RlOjE="){
                    name
                    address
                    city
                    state
                    phone
                    website
                    latitude
                    longitude
                }
            }
        """
        query_result = self.graphql_client.execute(query_string)
        expected_result = {
            "data": OrderedDict({
                "venue": OrderedDict(self.test_case_schema["venue_1"])
            })
        }
        self.assertEqual(query_result, expected_result)

class OrganizerQueriesTestCase(TestCase):

    graphql_client = Client(ROOT_SCHEMA)
    test_case_schema = {
        "organizer_1": {
            "name": "Organizer 1",
            "phone": "3202962997",
            "website": "https://www.organizer1.com",
            "email": "organizer1@organizers.com"
        },
        "organizer_2": {
            "name": "Organizer 2",
            "phone": "3212962998",
            "website": None,
            "email": None
        }
    }

    def setUp(self):
        """Configuración del caso de prueba."""
        TestSetup.setup()

    def test_all_organizers(self):
        query_string = """
            query{
                allOrganizers{
                    edges{
                        node{
                            name
                            phone
                            website
                            email
                        }
                    }
                }
            }
        """
        query_result = self.graphql_client.execute(query_string)
        expected_result = {
            "data": OrderedDict({
                "allOrganizers": OrderedDict({
                    "edges": [
                        OrderedDict({
                            "node": OrderedDict(
                                self.test_case_schema["organizer_1"]
                            )
                        }),
                        OrderedDict({
                            "node": OrderedDict(
                                self.test_case_schema["organizer_2"]
                            )
                        })
                    ]
                })
            })
        }
        self.assertEqual(query_result, expected_result)

    def test_single_organizer(self):
        query_string = """
            query{
                organizer(id: "T3JnYW5pemVyTm9kZTox"){
                    name
                    phone
                    website
                    email
                }
            }
        """
        query_result = self.graphql_client.execute(query_string)
        expected_result = {
            "data": OrderedDict({
                "organizer": OrderedDict(self.test_case_schema["organizer_1"])
            })
        }
        self.assertEqual(query_result, expected_result)

class EventQueriesTestCase(TestCase):

    graphql_client = Client(ROOT_SCHEMA)
    startDatetime = datetime(2019, 5, 15, 8, 00, 00, tzinfo=pytz.UTC)
    finishDatetime = datetime(2019, 5, 16, 8, 00, 00, tzinfo=pytz.UTC)
    test_case_schema = {
        "event_1": {
            "name": "Evento 1",
            "startDatetime": startDatetime.isoformat(),
            "finishDatetime": finishDatetime.isoformat(),
            "abstract": "Resumen evento 1",
            "description": "Descripción evento 1",
            "price": 1000.0,
            "website": "www.evento1.com",
            "limited": False,
            "active": True,
            "venue": OrderedDict({
                "name": "Lugar 1"
            })
        },
        "event_2": {
            "name": "Evento 2",
            "startDatetime": startDatetime.isoformat(),
            "finishDatetime": finishDatetime.isoformat(),
            "abstract": None,
            "description": "Descripción evento 2",
            "price": 0.0,
            "website": None,
            "limited": True,
            "active": False,
            "venue": OrderedDict({
                "name": "Lugar 2"
            })
        }
    }

    def setUp(self):
        """Configuración del caso de prueba."""
        TestSetup.setup()

    def test_all_events(self):
        query_string = """
            query{
                allEvents{
                    edges{
                        node{
                            name
                            startDatetime
                            finishDatetime
                            abstract
                            description
                            price
                            website
                            limited
                            active
                            venue{
                                name
                            }
                        }
                    }
                }
            }
        """
        query_result = self.graphql_client.execute(query_string)
        expected_result = {
            "data": OrderedDict({
                "allEvents": OrderedDict({
                    "edges": [
                        OrderedDict({
                            "node": OrderedDict(
                                self.test_case_schema["event_1"]
                            )
                        }),
                        OrderedDict({
                            "node": OrderedDict(
                                self.test_case_schema["event_2"]
                            )
                        })
                    ]
                })
            })
        }
        self.assertEqual(query_result, expected_result)

    def test_last_events(self):
        query_string = """
            query{
                lastEvents{
                    edges{
                        node{
                            name
                            startDatetime
                            finishDatetime
                            abstract
                            description
                            price
                            website
                            limited
                            active
                            venue{
                                name
                            }
                        }
                    }
                }
            }
        """
        query_result = self.graphql_client.execute(query_string)
        expected_result = {
            "data": OrderedDict({
                "lastEvents": OrderedDict({
                    "edges": [
                        OrderedDict({
                            "node": OrderedDict(
                                self.test_case_schema["event_2"]
                            )
                        }),
                        OrderedDict({
                            "node": OrderedDict(
                                self.test_case_schema["event_1"]
                            )
                        })
                    ]
                })
            })
        }
        self.assertEqual(query_result, expected_result)

    def test_recent_events(self):
        query_string = """
            query{
                recentEvents{
                    edges{
                        node{
                            name
                            startDatetime
                            finishDatetime
                            abstract
                            description
                            price
                            website
                            limited
                            active
                            venue{
                                name
                            }
                        }
                    }
                }
            }
        """
        query_result = self.graphql_client.execute(query_string)
        expected_result = {
            "data": OrderedDict({
                "recentEvents": OrderedDict({
                    "edges": [
                        OrderedDict({
                            "node": OrderedDict(
                                self.test_case_schema["event_1"]
                            )
                        }),
                        OrderedDict({
                            "node": OrderedDict(
                                self.test_case_schema["event_2"]
                            )
                        })
                    ]
                })
            })
        }
        self.assertEqual(query_result, expected_result)

    def test_single_event(self):
        query_string = """
            query{
                event(id: "RXZlbnROb2RlOjE="){
                    name
                    startDatetime
                    finishDatetime
                    abstract
                    description
                    price
                    website
                    limited
                    active
                    venue{
                        name
                    }
                }
            }
        """
        query_result = self.graphql_client.execute(query_string)
        expected_result = {
            "data": OrderedDict({
                "event": OrderedDict(self.test_case_schema["event_1"])
            })
        }
        self.assertEqual(query_result, expected_result)

# pylint: disable=E1101
class CategoryMutationsTestCase(JSONWebTokenTestCase):

    def setUp(self):
        TestSetup.setup()
        self.user = get_user_model().objects.create(username='test')
        self.client.authenticate(self.user)

    def test_update_category(self):
        query_string = """
            mutation($input: UpdateCategoryInput!){
                updateCategory(input: $input){updatedCategory{id}}
            }
        """
        variables = {
            "input": {
                "id": "Q2F0ZWdvcnlOb2RlOjE=",
                "category": {
                    "name": "Categoría 1 Updated",
                    "description": "Descripción categoría 1 Updated",
                }
            }
        }
        self.client.execute(query_string, variables=variables)
        categoria_1 = Category.objects.get(id=1)
        self.assertEqual(categoria_1.name, "Categoría 1 Updated")
        self.assertEqual(
            categoria_1.description,
            "Descripción categoría 1 Updated"
        )

class RelatedLinkMutationTestCase(JSONWebTokenTestCase):

    def setUp(self):
        """Configuración del caso de prueba."""
        TestSetup.setup()
        user = get_user_model().objects.create(username='test')
        self.client.authenticate(user)

    def test_add_related_links_to_category(self):
        query_string = """
            mutation($input: AddRelatedLinksToCategoryInput!){
                addRelatedLinksToCategory(input: $input){category{id}}
            }
        """
        variables = {
            "input": {
                "id": "Q2F0ZWdvcnlOb2RlOjE=",
                "relatedLinks": [
                    {
                        "name": "Link A",
                        "link": "www.linka.com",
                    },
                    {
                        "name": "Link B",
                        "link": "www.linkb.com",
                    }
                ]
            }
        }
        self.client.execute(query_string, variables=variables)
        rlink_a = RelatedLink.objects.get(name="Link A")
        rlink_b = RelatedLink.objects.get(name="Link B")
        self.assertEqual(rlink_a.link, "http://www.linka.com")
        self.assertEqual(rlink_b.link, "http://www.linkb.com")

    def test_delete_related_link(self):
        query_string = """
            mutation($input: DeleteRelatedLinkInput!){
                deleteRelatedLink(input: $input){success}
            }
        """
        variables = {
            "input": {
                "id": "UmVsYXRlZExpbmtOb2RlOjE="
            }
        }
        self.client.execute(query_string, variables=variables)
        with self.assertRaises(RelatedLink.DoesNotExist):
            RelatedLink.objects.get(id=1)

class VenueMutationsTestCase(JSONWebTokenTestCase):

    def setUp(self):
        TestSetup.setup()
        self.user = get_user_model().objects.create(username='test')
        self.client.authenticate(self.user)

    def test_create_venue(self):
        query_string = """
            mutation($input: CreateVenueInput!){
                createVenue(input: $input){newVenue{id}}
            }
        """
        variables = {
            "input": {
                "venue": {
                    "name": "Lugar 3",
                    "address": "Calle ABC3",
                    "city": "Caloto",
                    "state": "Cauca",
                    "latitude": 200.0,
                    "longitude": 300.0
                }
            }
        }
        self.client.execute(query_string, variables=variables)
        lugar_3 = Venue.objects.get(name="Lugar 3")
        self.assertEqual(lugar_3.address, "Calle ABC3")
        self.assertEqual(lugar_3.city, "Caloto")
        self.assertEqual(lugar_3.state, "Cauca")
        self.assertEqual(lugar_3.latitude, 200.0)
        self.assertEqual(lugar_3.longitude, 300.0)
        self.assertEqual(lugar_3.phone, "")
        self.assertEqual(lugar_3.website, "")

    def test_update_venue(self):
        query_string = """
            mutation($input: UpdateVenueInput!){
                updateVenue(input: $input){updatedVenue{id}}
            }
        """
        variables = {
            "input": {
                "id": "VmVudWVOb2RlOjE=",
                "venue": {
                    "name": "Updated",
                    "address": "Updated",
                    "city": "Caloto",
                    "state": "Tolima",
                    "phone": "3202962996",
                    "website": "https://lugar.com",
                    "latitude": 500.0,
                    "longitude": 600.0
                }
            }
        }
        self.client.execute(query_string, variables=variables)
        venue_1 = Venue.objects.get(id=1)
        self.assertEqual(venue_1.name, "Updated")
        self.assertEqual(venue_1.address, "Updated")
        self.assertEqual(venue_1.city, "Caloto")
        self.assertEqual(venue_1.state, "Tolima")
        self.assertEqual(venue_1.phone, "3202962996")
        self.assertEqual(venue_1.website, "https://lugar.com")
        self.assertEqual(venue_1.latitude, 500.0)
        self.assertEqual(venue_1.longitude, 600.0)

class OrganizerMutationsTestCase(JSONWebTokenTestCase):

    def setUp(self):
        TestSetup.setup()
        self.user = get_user_model().objects.create(username='test')
        self.client.authenticate(self.user)

    def test_create_organizer(self):
        query_string = """
            mutation($input: CreateOrganizerInput!){
                createOrganizer(input: $input){newOrganizer{id}}
            }
        """
        variables = {
            "input": {
                "organizer": {
                    "name": "Organizador 3"
                }
            }
        }
        self.client.execute(query_string, variables=variables)
        organizador_3 = Organizer.objects.get(name="Organizador 3")
        self.assertEqual(organizador_3.phone, "")
        self.assertEqual(organizador_3.website, "")
        self.assertEqual(organizador_3.email, "")

    def test_update_organizer(self):
        query_string = """
            mutation($input: UpdateOrganizerInput!){
                updateOrganizer(input: $input){updatedOrganizer{id}}
            }
        """
        variables = {
            "input": {
                "id": "T3JnYW5pemVyTm9kZTox",
                "organizer": {
                    "name": "Updated",
                    "phone": "Updated",
                    "website": "http://organizer.com",
                    "email": "email@organizer.com"
                }
            }
        }
        self.client.execute(query_string, variables=variables)
        organizador_1 = Organizer.objects.get(id=1)
        self.assertEqual(organizador_1.name, "Updated")
        self.assertEqual(organizador_1.phone, "Updated")
        self.assertEqual(organizador_1.website, "http://organizer.com")
        self.assertEqual(organizador_1.email, "email@organizer.com")

class EventMutationsTestCase(JSONWebTokenTestCase):

    def setUp(self):
        TestSetup.setup()
        self.user = get_user_model().objects.create(username='test')
        self.client.authenticate(self.user)

    def test_create_event(self):
        start_datetime = datetime(2019, 5, 15, 8, 00, 00, tzinfo=pytz.UTC)
        finish_datetime = datetime(2019, 5, 16, 8, 00, 00, tzinfo=pytz.UTC)
        query_string = """
            mutation($input: CreateEventInput!){
                createEvent(input: $input){newEvent{id}}
            }
        """
        variables = {
            "input": {
                "event": {
                    "name": "Evento 3",
                    "startDatetime": start_datetime.isoformat(),
                    "finishDatetime": finish_datetime.isoformat(),
                    "abstract": "Resumen evento 3",
                    "description": "Descripción evento 3",
                    "active": False,
                    "venue": "VmVudWVOb2RlOjE=",
                    "categories": [
                        "Q2F0ZWdvcnlOb2RlOjE=",
                        "Q2F0ZWdvcnlOb2RlOjI="
                    ],
                    "organizers": [
                        "T3JnYW5pemVyTm9kZToy",
                        "T3JnYW5pemVyTm9kZTox"
                    ]
                }
            }
        }
        self.client.execute(query_string, variables=variables)
        event_3 = Event.objects.get(name="Evento 3")
        self.assertEqual(event_3.start_datetime, start_datetime)
        self.assertEqual(event_3.finish_datetime, finish_datetime)
        self.assertEqual(event_3.abstract, "Resumen evento 3")
        self.assertEqual(event_3.description, "Descripción evento 3")
        self.assertEqual(event_3.active, False)
        self.assertEqual(event_3.venue.name, "Lugar 1")
        self.assertEqual(event_3.categories.get(id=1).name, "Categoría 1")
        self.assertEqual(event_3.categories.get(id=2).name, "Categoría 2")
        self.assertEqual(event_3.organizers.get(id=1).name, "Organizer 1")
        self.assertEqual(event_3.organizers.get(id=2).name, "Organizer 2")

    def test_update_event(self):
        start_datetime = datetime(2019, 5, 19, 8, 00, 00, tzinfo=pytz.UTC)
        finish_datetime = datetime(2019, 5, 19, 10, 00, 00, tzinfo=pytz.UTC)
        query_string = """
            mutation($input: UpdateEventInput!){
                updateEvent(input: $input){updatedEvent{id}}
            }
        """
        variables = {
            "input": {
                "id": "RXZlbnROb2RlOjE=",
                "event": {
                    "name": "Evento 1 Updated",
                    "startDatetime": start_datetime.isoformat(),
                    "finishDatetime": finish_datetime.isoformat(),
                    "abstract": "Resumen evento 1 Updated",
                    "description": "Descripción evento 1 Updated",
                    "price": 100.0,
                    "website": "https://updated.com",
                    "limited": True,
                    "active": False,
                    "venue": "VmVudWVOb2RlOjI=",
                    "categories": [
                        "Q2F0ZWdvcnlOb2RlOjE="
                    ],
                    "organizers": [
                        "T3JnYW5pemVyTm9kZToy"
                    ]
                }
            }
        }
        self.client.execute(query_string, variables=variables)
        event_1 = Event.objects.get(id=1)
        self.assertEqual(event_1.name, "Evento 1 Updated")
        self.assertEqual(event_1.start_datetime, start_datetime)
        self.assertEqual(event_1.finish_datetime, finish_datetime)
        self.assertEqual(event_1.abstract, "Resumen evento 1 Updated")
        self.assertEqual(event_1.description, "Descripción evento 1 Updated")
        self.assertEqual(event_1.price, 100.0)
        self.assertEqual(event_1.website, "https://updated.com")
        self.assertEqual(event_1.limited, True)
        self.assertEqual(event_1.active, False)
        self.assertEqual(event_1.venue.name, "Lugar 2")
        self.assertEqual(event_1.categories.get(id=1).name, "Categoría 1")
        self.assertEqual(event_1.categories.count(), 1)
        self.assertEqual(event_1.organizers.get(id=2).name, "Organizer 2")
        self.assertEqual(event_1.organizers.count(), 1)
