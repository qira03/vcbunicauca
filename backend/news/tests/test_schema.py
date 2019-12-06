"""Casos de prueba para el esquema GraphQL de noticias."""

import tempfile
from collections import OrderedDict

from django.contrib.auth import get_user_model
from django.test import TestCase
from graphene.test import Client
from graphql_jwt.testcases import JSONWebTokenTestCase

from news.models import Image, News
from news.tests.test_model import TestSetup as NewsTestSetup
from unicauca_vrcb.schema import ROOT_SCHEMA


class TestSetup():
    @staticmethod
    def setup():
        NewsTestSetup.setup()

class NewsQueriesTestCase(TestCase):

    graphql_client = Client(ROOT_SCHEMA)
    test_case_schema = {
        "noticia_1": {
            "name": "Noticia 1",
            "abstract": "Resumen de la noticia 1",
            "description": "Contenido de la noticia 1",
            "active": True
        },
        "noticia_2": {
            "name": "Noticia 2",
            "abstract": "Resumen de la noticia 2",
            "description": "Contenido de la noticia 2",
            "active": False
        }
    }

    def setUp(self):
        """Configuración del caso de prueba."""
        TestSetup.setup()

    def test_all_news(self):
        query_string = """
            query{
                allNews{
                    edges{
                        node{
                            name
                            abstract
                            description
                            active
                        }
                    }
                }
            }
        """
        query_result = self.graphql_client.execute(query_string)
        expected_result = {
            "data": {
                "allNews": {
                    "edges": [
                        {
                            "node": self.test_case_schema["noticia_1"]
                        },
                        {
                            "node": self.test_case_schema["noticia_2"]
                        }
                    ]
                }
            }
        }
        self.assertEqual(query_result, expected_result)

    def test_last_news(self):
        query_string = """
            query{
                lastNews{
                    edges{
                        node{
                            name
                            abstract
                            description
                            active
                        }
                    }
                }
            }
        """
        query_result = self.graphql_client.execute(query_string)
        expected_result = {
            "data": {
                "lastNews": {
                    "edges": [
                        {
                            "node": self.test_case_schema["noticia_2"]
                        },
                        {
                            "node": self.test_case_schema["noticia_1"]
                        }
                    ]
                }
            }
        }
        self.assertEqual(query_result, expected_result)

    def test_single_news(self):
        query_string = """
            query{
                news(id: "TmV3c05vZGU6MQ=="){
                    name
                    abstract
                    description
                    active
                }
            }
        """
        query_result = self.graphql_client.execute(query_string)
        expected_result = {
            "data": {
                "news": self.test_case_schema["noticia_1"]
            }
        }
        self.assertEqual(query_result, expected_result)

# pylint: disable=E1101
class NewsMutationsTestCase(JSONWebTokenTestCase):

    def setUp(self):
        TestSetup.setup()
        self.user = get_user_model().objects.create(username='test')
        self.client.authenticate(self.user)

    def test_create_news(self):
        query_string = """
            mutation(
                $noticia_A: CreateNewsInput!,
                $noticia_B: CreateNewsInput!
            ){
                noticia_A: createNews(input: $noticia_A){newNews{id}}
                noticia_B: createNews(input: $noticia_B){newNews{id}}
            }
        """
        variables = {
            "noticia_A": {
                "news": {
                    "name": "Noticia A",
                    "abstract": "Resumen noticia A",
                    "description": "Contenido noticia A"
                }
            },
            "noticia_B": {
                "news": {
                    "name": "Noticia B",
                    "abstract": "Resumen noticia B",
                    "description": "Contenido noticia B",
                    "active": False
                }
            }
        }
        self.client.execute(query_string, variables=variables)
        noticia_a = News.objects.get(name="Noticia A")
        noticia_b = News.objects.get(name="Noticia B")
        self.assertEqual(noticia_a.abstract, "Resumen noticia A")
        self.assertEqual(noticia_a.description, "Contenido noticia A")
        self.assertEqual(noticia_a.active, True)
        self.assertEqual(noticia_b.abstract, "Resumen noticia B")
        self.assertEqual(noticia_b.description, "Contenido noticia B")
        self.assertEqual(noticia_b.active, False)

    def test_update_news(self):
        query_string = """
            mutation(
                $noticia_1: UpdateNewsInput!,
                $noticia_2: UpdateNewsInput!){
                noticia_1: updateNews(input: $noticia_1){updatedNews{id}}
                noticia_2: updateNews(input: $noticia_2){updatedNews{id}}
            }
        """
        variables = {
            "noticia_1": {
                "id": "TmV3c05vZGU6MQ==",
                "news": {
                    "name": "Noticia 1 Updated",
                    "abstract": "Resumen noticia 1 Updated",
                    "description": "Descripción noticia 1 Updated"
                }
            },
            "noticia_2": {
                "id": "TmV3c05vZGU6Mg==",
                "news": {
                    "name": "Noticia 2 Updated",
                    "abstract": "Resumen noticia 2 Updated",
                    "description": "Descripción noticia 2 Updated",
                    "active": True
                }
            }
        }
        self.client.execute(
            query_string,
            variables=variables
        )
        noticia_1 = News.objects.get(id=1)
        noticia_2 = News.objects.get(id=2)
        self.assertEqual(noticia_1.name, "Noticia 1 Updated")
        self.assertEqual(noticia_1.abstract, "Resumen noticia 1 Updated")
        self.assertEqual(
            noticia_1.description,
            "Descripción noticia 1 Updated"
        )
        self.assertEqual(noticia_2.name, "Noticia 2 Updated")
        self.assertEqual(noticia_2.abstract, "Resumen noticia 2 Updated")
        self.assertEqual(
            noticia_2.description,
            "Descripción noticia 2 Updated"
        )

    # def test_add_images_to_post(self):
    #     pass

    # def test_update_image(self):
    #     pass

    def test_delete_image(self):
        query_string = """
            mutation deleteImage($input: DeleteImageInput!){
                deleteImage(input: $input){success}
            }
        """
        variables = {"input": {"id": "SW1hZ2VOb2RlOjE="}}
        self.client.execute(query_string, variables=variables)
        with self.assertRaises(Image.DoesNotExist):
            Image.objects.get(id=1)
