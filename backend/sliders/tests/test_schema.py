"""Casos de prueba para el esquema GraphQL de sliders."""

from collections import OrderedDict

from django.contrib.auth import get_user_model
from django.test import TestCase
from graphene.test import Client
from graphql_jwt.testcases import JSONWebTokenTestCase

from sliders.models import Slider
from sliders.tests.test_model import TestSetup as SliderTestSetup
from unicauca_vrcb.schema import ROOT_SCHEMA


class TestSetup():
    @staticmethod
    def setup():
        SliderTestSetup.setup()

class SliderQueriesTestCase(TestCase):

    graphql_client = Client(ROOT_SCHEMA)
    test_case_schema = {
        "slider_1": {
            "name": "Slider 1",
            "position": "NONE",
            "description": "Descripción slider 1",
            "active": True
        },
        "slider_2": {
            "name": "Slider 2",
            "position": "HOME",
            "description": "Descripción slider 2",
            "active": False
        }
    }

    def setUp(self):
        """Configuración del caso de prueba."""
        TestSetup.setup()

    def test_all_sliders(self):
        query_string = """
            query{
                allSliders{
                    edges{
                        node{
                            name
                            position
                            description
                            active
                        }
                    }
                }
            }
        """
        query_result = self.graphql_client.execute(query_string)
        expected_result = {
            "data": OrderedDict({
                "allSliders": OrderedDict({
                    "edges": [
                        OrderedDict({
                            "node": OrderedDict(
                                self.test_case_schema["slider_1"]
                            )
                        }),
                        OrderedDict({
                            "node": OrderedDict(
                                self.test_case_schema["slider_2"]
                            )
                        })
                    ]
                })
            })
        }
        self.assertEqual(query_result, expected_result)

    def test_single_slider(self):
        query_string = """
            query{
                slider(id: "U2xpZGVyTm9kZTox"){
                    name
                    position
                    description
                    active
                }
            }
        """
        query_result = self.graphql_client.execute(query_string)
        expected_result = {
            "data": OrderedDict({
                "slider": OrderedDict(
                    self.test_case_schema["slider_1"]
                )
            })
        }
        self.assertEqual(query_result, expected_result)

# pylint: disable=E1101
class SliderMutationsTestCase(JSONWebTokenTestCase):

    def setUp(self):
        TestSetup.setup()
        self.user = get_user_model().objects.create(username='test')
        self.client.authenticate(self.user)

    def test_create_slider(self):
        query_string = """
            mutation(
                $slider_A: CreateSliderInput!,
                $slider_B: CreateSliderInput!
            ){
                slider_A: createSlider(input: $slider_A){newSlider{id}}
                slider_B: createSlider(input: $slider_B){newSlider{id}}
            }
        """
        variables = {
            "slider_A": {
                "slider": {
                    "name": "Slider A",
                    "position": "SECTION",
                    "description": "Descripción slider A"
                }
            },
            "slider_B": {
                "slider": {
                    "name": "Slider B",
                    "position": "FOOTER",
                    "description": "Descripción slider B",
                    "active": False
                }
            }
        }
        self.client.execute(query_string, variables=variables)
        slider_a = Slider.objects.get(name="Slider A")
        slider_b = Slider.objects.get(name="Slider B")
        self.assertEqual(slider_a.position, "SECTION")
        self.assertEqual(slider_a.description, "Descripción slider A")
        self.assertEqual(slider_a.active, True)
        self.assertEqual(slider_b.position, "FOOTER")
        self.assertEqual(slider_b.description, "Descripción slider B")
        self.assertEqual(slider_b.active, False)

    def test_update_slider(self):
        query_string = """
            mutation(
                $slider_1: UpdateSliderInput!,
                $slider_2: UpdateSliderInput!
            ){
                slider_1: updateSlider(input: $slider_1){updatedSlider{id}}
                slider_2: updateSlider(input: $slider_2){updatedSlider{id}}
            }
        """
        variables = {
            "slider_1": {
                "id": "U2xpZGVyTm9kZTox",
                "slider": {
                    "name": "Slider 1 Updated",
                    "position": "UPDATED",
                    "description": "Descripción slider 1 Updated"
                }
            },
            "slider_2": {
                "id": "U2xpZGVyTm9kZToy",
                "slider": {
                    "name": "Slider 2 Updated",
                    "position": "2UPDATED",
                    "description": "Descripción slider 2 Updated",
                    "active": True
                }
            }
        }
        self.client.execute(query_string, variables=variables)
        slider_1 = Slider.objects.get(id=1)
        slider_2 = Slider.objects.get(id=2)
        self.assertEqual(slider_1.name, "Slider 1 Updated")
        self.assertEqual(slider_1.position, "UPDATED")
        self.assertEqual(slider_1.description, "Descripción slider 1 Updated")
        self.assertEqual(slider_2.name, "Slider 2 Updated")
        self.assertEqual(slider_2.position, "2UPDATED")
        self.assertEqual(slider_2.description, "Descripción slider 2 Updated")
        self.assertEqual(slider_2.active, True)
