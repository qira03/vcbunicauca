"""Casos de prueba para el esquema GraphQL de usuarios."""

from collections import OrderedDict

from django.contrib.auth.models import User
from graphql_jwt.testcases import JSONWebTokenTestCase


class TestSetup():
    @staticmethod
    def setup():
        User.objects.create(
            username="usuario1",
            email="usuario1@users.com",
            password="usuario1pwd"
        )
        User.objects.create(
            username="usuario2",
            email="usuario2@users.com",
            password="usuario2pwd",
            first_name="Dummy",
            last_name="User"
        )

# pylint: disable=E1101
class UserQueriesTestCase(JSONWebTokenTestCase):

    test_case_schema = {
        "usuario_1": {
            "username": "usuario1",
            "email": "usuario1@users.com",
            "firstName": "",
            "lastName": "",
            "isSuperuser": False,
            "isStaff": False,
            "isActive": True

        },
        "usuario_2": {
            "username": "usuario2",
            "email": "usuario2@users.com",
            "firstName": "Dummy",
            "lastName": "User",
            "isSuperuser": False,
            "isStaff": False,
            "isActive": True
        }
    }

    def setUp(self):
        """Configuración del caso de prueba."""
        TestSetup.setup()
        usuario_1 = User.objects.get(id=1)
        self.client.authenticate(usuario_1)

    def test_all_users(self):
        query_string = """
            query{
                allUsers{
                    edges{
                        node{
                            username
                            email
                            firstName
                            lastName
                            isSuperuser
                            isStaff
                            isActive
                        }
                    }
                }
            }
        """
        query_result = self.client.execute(query_string)
        expected_result = OrderedDict({
            "allUsers": OrderedDict({
                "edges": [
                    OrderedDict({
                        "node": OrderedDict(
                            self.test_case_schema["usuario_1"]
                        )
                    }),
                    OrderedDict({
                        "node": OrderedDict(
                            self.test_case_schema["usuario_2"]
                        )
                    })
                ]
            })
        })
        self.assertEqual(dict(query_result.data), expected_result)

    def test_single_user(self):
        query_string = """
            query{
                user(id: "VXNlck5vZGU6MQ=="){
                    username
                    email
                    firstName
                    lastName
                    isSuperuser
                    isStaff
                    isActive
                }
            }
        """
        query_result = self.client.execute(query_string)
        expected_result = OrderedDict({
            "user": OrderedDict(self.test_case_schema["usuario_1"])
        })
        self.assertEqual(dict(query_result.data), expected_result)

# pylint: disable=E1101
class UserMutationsTestCase(JSONWebTokenTestCase):

    def setUp(self):
        TestSetup.setup()
        user_1 = User.objects.get(id=1)
        self.client.authenticate(user_1)

    def test_create_user(self):
        query_string = """
            mutation($user_A: CreateUserInput!, $user_B: CreateUserInput!){
                user_A: createUser(input: $user_A){newUser{id}}
                user_B: createUser(input: $user_B){newUser{id}}
            }
        """
        variables = {
            "user_A": {
                "user": {
                    "username": "usuario3",
                    "email": "usuario3@users.com",
                    "password": "dummypassword3"
                }
            },
            "user_B": {
                "user": {
                    "username": "usuario4",
                    "email": "usuario4@users.com",
                    "password": "dummypassword4",
                    "firstName": "Awesome",
                    "lastName": "User"
                }
            }
        }
        self.client.execute(query_string, variables=variables)
        user_a = User.objects.get(username="usuario3")
        user_b = User.objects.get(username="usuario4")
        self.assertEqual(user_a.email, "usuario3@users.com")
        self.assertTrue(user_a.check_password("dummypassword3"))
        self.assertEqual(user_b.email, "usuario4@users.com")
        self.assertTrue(user_b.check_password("dummypassword4"))
        self.assertEqual(user_b.first_name, "Awesome")
        self.assertEqual(user_b.last_name, "User")

    def test_update_user(self):
        query_string = """
            mutation($user_1: UpdateUserInput!, $user_2: UpdateUserInput!){
                user_1: updateUser(input: $user_1){updatedUser{id}}
                user_2: updateUser(input: $user_2){updatedUser{id}}
            }
        """
        variables = {
            "user_1": {
                "id": "VXNlck5vZGU6MQ==",
                "user": {
                    "email": "updated1@users.com",
                    "firstName": "UpdatedFN1",
                    "lastName": "UpdatedLN1",
                }
            },
            "user_2": {
                "id": "VXNlck5vZGU6Mg==",
                "user": {
                    "email": "updated2@users.com",
                    "firstName": "UpdatedFN2",
                    "lastName": "UpdatedLN2",
                    "active": False
                }
            }
        }
        self.client.execute(query_string, variables=variables)
        user_1 = User.objects.get(id=1)
        user_2 = User.objects.get(id=2)
        self.assertEqual(user_1.email, "updated1@users.com")
        self.assertEqual(user_1.first_name, "UpdatedFN1")
        self.assertEqual(user_1.last_name, "UpdatedLN1")
        self.assertEqual(user_2.email, "updated2@users.com")
        self.assertEqual(user_2.first_name, "UpdatedFN2")
        self.assertEqual(user_2.last_name, "UpdatedLN2")
        self.assertEqual(user_2.is_active, False)

    def test_update_user_password(self):
        query_string = """
            mutation($input: UpdateUserPasswordInput!){
                updateUserPassword(input: $input){updatedUser{id}}
            }
        """
        variables = {
            "input": {
                "id": "VXNlck5vZGU6MQ==",
                "password": "newPassword"
            }
        }
        self.client.execute(query_string, variables=variables)
        user_1 = User.objects.get(id=1)
        self.assertTrue(user_1.check_password("newPassword"))
