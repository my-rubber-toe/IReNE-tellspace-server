import unittest

from utils.validators import CreateDocumentValidator
from marshmallow import ValidationError


class CreateDocumentsValidatorTest(unittest.TestCase):
    def setUp(self) -> None:
        self.test_validator = CreateDocumentValidator()

    def test_correct_data(self):
        """CreateDocumentsValidatorTest: Given data is correct."""

        correct_data = {
            "actors": [
                {
                    "first_name": "name1",
                    "last_name": "lastname1",
                    "role": "some"
                }
            ],

            "authors": [
                {
                    "first_name": "name1",
                    "last_name": "lastname1",
                    "email": "email@email.com",
                    "faculty": "somefaculty"
                }
            ],

            "incident_date": "2020-02-15",

            "damage_type": ["damage1", "damage2", "damage3"],

            "infrastructure_type": ["infrastrucutre1", "infrastructure2", "infrastructure3"],

            "title": "Some Title"
        }

        self.assertIsNotNone(self.test_validator.load(correct_data))


    def test_incorrect_data(self):
        """CreateDocumentsValidatorTest: Given data is incorrect. ValidationError is raised."""

        incorrect_data = {
            1: {},
            2: {
                "actors": [], #empty actors
                "authors": [
                    {
                        "first_name": "name1",
                        "last_name": "lastname1",
                        "email": "email@email.com",
                        "faculty": "somefaculty"
                    }
                ],

                "incident_date": "2020-02-15",

                "damage_type": ["damage1", "damage2", "damage3"],

                "infrastructure_type": ["infrastrucutre1", "infrastructure2", "infrastructure3"],

                "title": "Some Title"
            }
        }

        for x in range(1, len(incorrect_data) + 1):
            with self.assertRaises(ValidationError):
                self.test_validator.load(incorrect_data[x])
