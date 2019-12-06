"""Casos de prueba para la aplicación de eventos."""

import tempfile
from datetime import date, datetime

import pytz
from django.core.exceptions import ValidationError
from django.db import IntegrityError
from django.template.defaultfilters import slugify
from django.test import TestCase

from events.models import Category, Event, Organizer, RelatedLink, Venue


class TestSetup():
    @staticmethod
    def setup():
        categoria_1 = Category.objects.create(
            name="Categoría 1",
            description="Descripción categoría 1",
            image=tempfile.NamedTemporaryFile(
                suffix=".jpg",
                dir="./media"
            ).name
        )
        categoria_2 = Category.objects.create(
            name="Categoría 2",
            description="Descripción categoría 2",
            image=tempfile.NamedTemporaryFile(
                suffix=".jpg",
                dir="./media"
            ).name
        )
        RelatedLink.objects.create(
            name="Link 1",
            link="www.link1.com",
            category=categoria_2
        )
        RelatedLink.objects.create(
            name="Link 2",
            link="www.link2.com",
            category=categoria_2
        )
        lugar_1 = Venue.objects.create(
            name="Lugar 1",
            address="Calle A 11",
            city="Popayán",
            state="Cauca",
            phone="3202962997",
            website="https://www.venue1.com",
            latitude=1.100,
            longitude=2.200
        )
        lugar_2 = Venue.objects.create(
            name="Lugar 2",
            address="Valle ABC 123",
            city="Popayán",
            state="Cauca",
            latitude=3.300,
            longitude=4.400
        )
        organizador_1 = Organizer.objects.create(
            name="Organizer 1",
            phone="3202962997",
            website="https://www.organizer1.com",
            email="organizer1@organizers.com"
        )
        organizador_2 = Organizer.objects.create(
            name="Organizer 2",
            phone="3212962998"
        )
        evento_1 = Event.objects.create(
            name="Evento 1",
            start_datetime=datetime(2019, 5, 15, 8, 00, 00, tzinfo=pytz.UTC),
            finish_datetime=datetime(2019, 5, 16, 8, 00, 00, tzinfo=pytz.UTC),
            abstract="Resumen evento 1",
            description="Descripción evento 1",
            price=1000,
            website="www.evento1.com",
            venue=lugar_1
        )
        evento_1.organizers.add(organizador_1)
        evento_1.categories.add(categoria_1)
        evento_2 = Event.objects.create(
            name="Evento 2",
            start_datetime=datetime(2019, 5, 15, 8, 00, 00, tzinfo=pytz.UTC),
            finish_datetime=datetime(2019, 5, 16, 8, 00, 00, tzinfo=pytz.UTC),
            description="Descripción evento 2",
            limited=True,
            active=False,
            venue=lugar_2
        )
        evento_2.organizers.add(organizador_1, organizador_2)
        evento_2.categories.add(categoria_1, categoria_2)

class CategoryTestCase(TestCase):
    """Caso de prueba para el modelo de Category."""

    def setUp(self):
        """Configuración del caso de prueba."""
        TestSetup.setup()

    def test_name_length_validation(self):
        """Comprueba la longitud del nombre."""
        category = Category(
            name="Officia mollit esse eiusmod dolor mollit Lorem. Ut sint "\
                "deseruntalli",
            slug=slugify("Officia mollit esse eiusmod dolor mollit Lorem."),
            description="Lorem ipsum dolor sit amet, consectetu",
            image=tempfile.NamedTemporaryFile(suffix=".jpg").name
        )
        with self.assertRaisesRegex(ValidationError, "(name).*(64)"):
            category.full_clean()

    def test_slug(self):
        """Comprueba que el slug se cree de forma correcta."""
        category = Category.objects.get(name="Categoría 1")
        slug_addon = "-{date.month}-{date.year}".format(date=date.today())
        self.assertEqual(category.slug, "categoria-1" + slug_addon)

    def test_slug_unique(self):
        """Comprueba que el slug sea único."""
        category = Category(
            name="Categoría 1",
            description="Descripción categoría 1",
            image=tempfile.NamedTemporaryFile(suffix=".jpg").name
        )
        with self.assertRaises(IntegrityError):
            category.save()

    def test_description_length_validation(self):
        """Comprueba la longitud de la descripción."""
        category = Category(
            name="Officia mollit esse eiusmod dolor mollit Lorem.",
            slug=slugify("Officia mollit esse eiusmod dolor mollit Lorem."),
            description="Lorem ipsum dolor sit amet, consectetuer adipiscing "\
                "elit. Aenean commodo ligula eget dolor. Aenean massa. Cum "\
                "sociis natoque penatibus et magnis dis parturient montes, na",
            image=tempfile.NamedTemporaryFile(suffix=".jpg").name
        )
        with self.assertRaisesRegex(ValidationError, "(description).*(140)"):
            category.full_clean()

class RelatedLinkTestCase(TestCase):
    """Caso de prueba para el modelo de RelatedLink."""

    def setUp(self):
        """Configuración del caso de prueba."""
        TestSetup.setup()

    def test_name_length_validation(self):
        """Comprueba la longitud del nombre."""
        rlink = RelatedLink(
            name="Officia mollit esse eiusmod dolor mollit Lorem. Ut sint "\
                "deseruntalli Officia mollit esse eiusmod dolor mollit Lorem"\
                "deseruntalli Officia mollit esse eiusmod dolor mollit Lorem",
            link="www.test.com",
            category=Category.objects.get(id=1)
        )
        with self.assertRaisesRegex(ValidationError, "(name).*(120)"):
            rlink.full_clean()

    def test_link_validation(self):
        """Comprueba la validez del link del enlace relacionado."""
        rlink = RelatedLink(
            name="Link test",
            link="esto no es una url",
            category=Category.objects.get(id=1)
        )
        with self.assertRaisesRegex(ValidationError, "(link).*(URL)") as pedo:
            rlink.full_clean()

class VenueTestCase(TestCase):
    """Caso de prueba para el modelo de Venue."""

    def setUp(self):
        """Configuración del caso de prueba."""
        TestSetup.setup()

    def test_name_length(self):
        """Prueba de longitud del nombre."""
        venue = Venue(
            name="Lorem ipsum dolor sit amet, consectetuer adipiscing elit. "\
                "Aenean commodo ligula eget dolor aenean",
            address="Calle abc",
            latitude=1.123,
            longitude=1.123
        )
        with self.assertRaisesRegex(ValidationError, "(name).*(96)"):
            venue.full_clean()

    def test_address_length(self):
        """Prueba la longitud de la dirección."""
        venue = Venue(
            name="Lugar 1",
            address="Lorem ipsum dolor sit amet, consectetuer adipiscing "\
                "elit Aenean commo",
            latitude=1.123,
            longitude=1.123
        )
        with self.assertRaisesRegex(ValidationError, "(address).*(64)"):
            venue.full_clean()

    def test_city_length(self):
        """Prueba la longitud de la ciudad."""
        venue = Venue(
            name="Lugar 1",
            address="Calle abc",
            city="Lorem ipsum dolor sit amet, consect",
            latitude=1.123,
            longitude=1.123
        )
        with self.assertRaisesRegex(ValidationError, "(city).*(32)"):
            venue.full_clean()

    def test_city_default(self):
        """Prueba el valor predeterminado de la ciudad."""
        venue = Venue.objects.get(name="Lugar 1")
        self.assertEqual(venue.city, "Popayán")

    def test_state_length(self):
        """Prueba la longitud del departamento."""
        venue = Venue(
            name="Lugar 1",
            address="Calle abc",
            state="Lorem ipsum dolor sit amet, consect",
            latitude=1.123,
            longitude=1.123
        )
        with self.assertRaisesRegex(ValidationError, "(state).*(32)"):
            venue.full_clean()

    def test_state_default(self):
        """Comprueba el valor predeterminado del departamento."""
        venue = Venue.objects.get(name="Lugar 1")
        self.assertEqual(venue.state, "Cauca")

    def test_phone_length(self):
        """Comprueba la longitud del teléfono."""
        venue = Venue(
            name="Lugar 1",
            address="Calle abc",
            phone="Lorem ipsum dolor si",
            latitude=1.123,
            longitude=1.123
        )
        with self.assertRaisesRegex(ValidationError, "(phone).*(18)"):
            venue.full_clean()

    def test_website_url(self):
        """Comprueba que el website sea una URL."""
        venue = Venue(
            name="Lugar 1",
            address="Calle abc",
            website="No es una URL",
            latitude=1.123,
            longitude=1.123
        )
        with self.assertRaisesRegex(ValidationError, "(website).*(URL)"):
            venue.full_clean()

    def test_latitude_float(self):
        """Comprueba que la latitud sea un número flotante."""
        venue = Venue(
            name="Lugar 1",
            address="Calle abc",
            latitude="Cadena",
            longitude=1.123
        )
        with self.assertRaisesRegex(ValidationError, "(latitude)"):
            venue.full_clean()

    def test_longitude_float(self):
        """Comprueba que la longitud sea un número flotante."""
        venue = Venue(
            name="Lugar 1",
            address="Calle abc",
            latitude=1.123,
            longitude="Cadena"
        )
        with self.assertRaisesRegex(ValidationError, "(longitude)"):
            venue.full_clean()

class OrganizerTestCase(TestCase):
    """Caso de prueba del organizador."""

    def setUp(self):
        """Configuración del caso de prueba."""
        TestSetup.setup()

    def test_name_length(self):
        """Prueba la longitud del nombre."""
        organizer = Organizer(
            name="Lorem ipsum dolor sit amet, consectetuer adipiscing elit "\
                "aenean commodo ligula eget dolor"
        )
        with self.assertRaisesRegex(ValidationError, "(name).*(80)"):
            organizer.full_clean()

    def test_phone_length(self):
        """Comprueba la longitud del teléfono."""
        organizer = Organizer(
            name="Organizador 1",
            phone="Lorem ipsum dolor si"
        )
        with self.assertRaisesRegex(ValidationError, "(phone).*(18)"):
            organizer.full_clean()

    def test_website_url(self):
        """Comprueba que el website sea una URL."""
        organizer = Organizer(
            name="Lugar 1",
            website="No es una URL",
        )
        with self.assertRaisesRegex(ValidationError, "(website).*(URL)"):
            organizer.full_clean()

    def test_email_url(self):
        """Comprueba que el email sea una email válido."""
        organizer = Organizer(
            name="Lugar 1",
            email="No es un email",
        )
        with self.assertRaisesRegex(ValidationError, "(email)"):
            organizer.full_clean()

class EventTestCase(TestCase):
    """Caso de prueba para el modelo de Event."""

    def setUp(self):
        """Configuración del caso de prueba."""
        TestSetup.setup()

    def test_name_length_validation(self):
        """Comprueba la longitud del nombre."""
        venue = Venue.objects.get(name="Lugar 1")
        event = Event(
            name="Officia mollit esse eiusmod dolor mollit Lorem. Ut sint "\
                "deserunta",
            start_datetime=datetime(2019, 5, 15, 8, 00, 00, tzinfo=pytz.UTC),
            finish_datetime=datetime(2019, 5, 16, 14, 00, 00, tzinfo=pytz.UTC),
            description="Descripción del evento",
            venue=venue
        )
        with self.assertRaisesRegex(ValidationError, "(name).*(64)"):
            event.full_clean()

    def test_slug_gen(self):
        """Comprueba que el slug se cree de forma correcta."""
        event = Event.objects.get(name="Evento 1")
        slug_addon = "-{date.month}-{date.year}".format(date=date.today())
        self.assertEqual(event.slug, slugify(event.name) + slug_addon)

    def test_slug_unique(self):
        """Comprueba que el slug sea único."""
        venue = Venue.objects.get(name="Lugar 1")
        event = Event(
            name="Evento 1",
            start_datetime=datetime(2019, 5, 15, 8, 00, 00, tzinfo=pytz.UTC),
            finish_datetime=datetime(2019, 5, 16, 14, 00, 00, tzinfo=pytz.UTC),
            description="Descripción del evento",
            venue=venue
        )
        with self.assertRaises(IntegrityError):
            event.save()

    def test_start_date(self):
        """Comprueba que la fecha de inicio corresponda a una fecha y hora."""
        venue = Venue.objects.get(name="Lugar 1")
        event = Event(
            name="Evento 1",
            slug="evento-2",
            start_datetime="Esto no es una fecha",
            finish_datetime=datetime(2019, 5, 16, 14, 00, 00, tzinfo=pytz.UTC),
            description="Descripción del evento",
            venue=venue
        )
        with self.assertRaisesRegex(ValidationError, "start_date"):
            event.full_clean()

    def test_finish_date(self):
        """Comprueba que la fecha de cierre corresponda a una fecha y hora."""
        venue = Venue.objects.get(name="Lugar 1")
        event = Event(
            name="Evento 1",
            slug="evento-2",
            start_datetime=datetime(2019, 5, 16, 14, 00, 00, tzinfo=pytz.UTC),
            finish_datetime="Esto no es una fecha",
            description="Descripción del evento",
            venue=venue
        )
        with self.assertRaisesRegex(ValidationError, "finish_datetime"):
            event.full_clean()

    def test_finish_datetime(self):
        """Comprueba que las fechas de finalización sean válidas."""
        venue = Venue.objects.get(name="Lugar 1")
        event = Event(
            name="Evento 3",
            slug="event-3",
            start_datetime=datetime(2019, 5, 15, 8, 00, 00, tzinfo=pytz.UTC),
            finish_datetime=datetime(2019, 4, 11, 6, 00, 00, tzinfo=pytz.UTC),
            abstract="Resumen evento 2",
            description="Descripción evento 2",
            venue=venue
        )
        with self.assertRaisesRegex(ValidationError, "finish_datetime"):
            event.save()

    def test_abstract_length(self):
        """Comprueba la longitud del resumen."""
        venue = Venue.objects.get(name="Lugar 1")
        event = Event(
            name="Evento 4",
            slug="evento-4",
            start_datetime=datetime(2019, 5, 15, 8, 00, 00, tzinfo=pytz.UTC),
            finish_datetime=datetime(2019, 5, 16, 14, 00, 00, tzinfo=pytz.UTC),
            abstract="Lorem ipsum dolor sit amet, consectetuer adipiscing "\
                "elit. Aenean commodo ligula eget dolor. Aenean massa. Cum "\
                "sociis natoque penatibus et magnis dis",
            description="Descripción del evento",
            venue=venue
        )
        with self.assertRaisesRegex(ValidationError, "(abstract).*(140)"):
            event.full_clean()

    def test_price_default(self):
        """Prueba el valor predeterminado del precio."""
        event = Event.objects.get(name="Evento 2")
        self.assertAlmostEqual(event.price, 0)

    def test_website_url(self):
        """Comprueba que el website sea una URL."""
        venue = Venue.objects.get(name="Lugar 1")
        event = Event(
            name="Evento 4",
            slug="evento-4",
            start_datetime=datetime(2019, 5, 16, 14, 00, 00, tzinfo=pytz.UTC),
            finish_datetime=datetime(2019, 5, 17, 14, 00, 00, tzinfo=pytz.UTC),
            website="Esto no es una URL",
            description="Descripción del evento",
            venue=venue
        )
        with self.assertRaisesRegex(ValidationError, "(website).*(URL)"):
            event.full_clean()

    def test_limited_default(self):
        """Prueba el valor predeterminado de limited."""
        event = Event.objects.get(name="Evento 1")
        self.assertEqual(event.limited, False)

    def test_active_default(self):
        """Prueba el valor predeterminado de active."""
        event = Event.objects.get(name="Evento 1")
        self.assertEqual(event.active, True)
