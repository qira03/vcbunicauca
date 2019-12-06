"""Casos de prueba para la aplicación de Sliders."""

from django.core.exceptions import ValidationError
from django.test import TestCase

from sliders.models import Slider


class TestSetup():
    @staticmethod
    def setup():
        Slider.objects.create(
            name="Slider 1",
            description="Descripción slider 1"
        )
        Slider.objects.create(
            name="Slider 2",
            position="HOME",
            description="Descripción slider 2",
            active=False
        )

class SliderTestCase(TestCase):
    """Caso de prueba para el modelo de Slider."""

    def setUp(self):
        """Configuración del caso de prueba."""
        TestSetup.setup()

    def test_name_length_validation(self):
        """Comprueba la longitud del nombre."""
        slider = Slider(
            name="Officia mollit esse eiusmod dolor mollit Lorem. Ut sint"\
                "deserunta eiusmod dolor mollit",
            description="Officia mollit",
        )
        with self.assertRaisesRegex(ValidationError, "(name).*(64)"):
            slider.full_clean()

    def test_position_length_validation(self):
        """Comprueba la longitud de la posición."""
        slider = Slider(
            name="A single slider",
            position="Officia mollit esse eiusmod dolor mollit Lorem. Ut sint"\
                "deserunta eiusmod dolor mollit deserunta eiusmod dolor",
            description="Officia mollit",
        )
        with self.assertRaisesRegex(ValidationError, "(position).*(100)"):
            slider.full_clean()

    def test_position_default(self):
        """Comprueba el valor predeterminado del campo position."""
        slider = Slider.objects.get(name="Slider 1")
        self.assertEqual(slider.position, "NONE")

    def test_description_length_validation(self):
        """Comprueba la longitud de la descripción."""
        slider = Slider(
            name="Officia mollit esse eiusmod",
            description="Officia mollit esse eiusmod dolor mollit Lorem. Ut"\
                "sint deserunta eiusmod dolor mollit officia mollit esse"\
                "eiusmod dolor mollit Lorem officia mollit esse eiusmod dolor"
        )
        with self.assertRaisesRegex(ValidationError, "(description).*(144)"):
            slider.full_clean()

    def test_active_default(self):
        """Comprueba el valor predeterminado del campo active."""
        slider = Slider.objects.get(name="Slider 1")
        self.assertEqual(slider.active, True)
