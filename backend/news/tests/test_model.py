"""Casos de prueba para el modelo de noticias."""

import tempfile
from datetime import date

from django.core.exceptions import ValidationError
from django.db import IntegrityError
from django.template.defaultfilters import slugify
from django.test import TestCase

from news.models import Image, News


class TestSetup():
    """Configura el contenido inicial de los casos de prueba."""

    @staticmethod
    def setup():
        news_1 = News.objects.create(
            name="Noticia 1",
            abstract="Resumen de la noticia 1",
            description="Contenido de la noticia 1"
        )
        news_2 = News.objects.create(
            name="Noticia 2",
            abstract="Resumen de la noticia 2",
            description="Contenido de la noticia 2",
            active=False
        )
        Image.objects.create(
            principal=False,
            image_file=tempfile.NamedTemporaryFile(
                suffix=".jpg",
                dir="./media"
            ).name,
            post=news_1
        )
        Image.objects.create(
            principal=True,
            image_file=tempfile.NamedTemporaryFile(
                suffix=".jpg",
                dir="./media"
            ).name,
            post=news_1
        )
        Image.objects.create(
            principal=False,
            image_file=tempfile.NamedTemporaryFile(
                suffix=".jpg",
                dir="./media"
            ).name,
            post=news_1
        )
        Image.objects.create(
            image_file=tempfile.NamedTemporaryFile(
                suffix=".png",
                dir="./media"
            ).name,
            post=news_2
        )

class NewsTestCase(TestCase):
    """Caso de prueba para el modelo de News."""

    def setUp(self):
        """Configuración del caso de prueba."""
        TestSetup.setup()

    def test_name_length_validation(self):
        """Comprueba la longitud del nombre."""
        news = News(
            name="Officia mollit esse eiusmod dolor mollit Lorem. Ut sint"\
                "deserunta eiusmod dolor mollit",
            slug="test-slug",
            abstract="Officia mollit",
            description="Nulla consectetur"
        )
        with self.assertRaisesRegex(ValidationError, "(name).*(64)"):
            news.full_clean()

    def test_slug_gen(self):
        """Comprueba que el slug se cree de forma correcta."""
        news = News.objects.get(name="Noticia 1")
        slug_addon = "-{date.month}-{date.year}".format(date=date.today())
        self.assertEqual(news.slug, slugify(news.name) + slug_addon)

    def test_slug_unique(self):
        """Comprueba que el slug sea único."""
        news = News(
            name="Noticia 1",
            abstract="Resumen de la noticia 1",
            description="Contenido de la noticia 1"
        )
        with self.assertRaises(IntegrityError):
            news.save()

    def test_abstract_length_validation(self):
        """Comprueba la longitud del resumen."""
        news = News(
            name="Officia mollit esse eiusmod dolor mollit Lorem.",
            slug=slugify("Officia mollit esse eiusmod dolor mollit Lorem."),
            abstract="Lorem ipsum dolor sit amet, consectetuer adipiscing"\
                "elit. Aenean commodo ligula eget dolor. Aenean massa. Cum"\
                "sociis natoque penatibus et magnis dis parturient montes, na",
            description="Nulla consectetur"
        )
        with self.assertRaisesRegex(ValidationError, "(abstract).*(140)"):
            news.full_clean()

    def test_active_default(self):
        """Comprueba el valor predeterminado de las noticias."""
        news = News.objects.get(name="Noticia 1")
        self.assertEqual(news.active, True)

class ImageTestCase(TestCase):
    """Caso de prueba para el modelo de Image."""

    def setUp(self):
        """Configuración del caso de prueba."""
        TestSetup.setup()

    def test_principal_default(self):
        """Comprueba el valor predeterminado del atributo principal."""
        news = News.objects.get(name="Noticia 2")
        self.assertEqual(news.images.first().principal, False)
