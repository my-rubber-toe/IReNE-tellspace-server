import unittest
import json
from datetime import date
from utils.validators import *

from marshmallow import ValidationError


class GetDocumentsValidatorTest(unittest.TestCase):

    def setUp(self) -> None:
        self.test_validator = GetDocumentsValidator()

    def tearDown(self) -> None:
        """Set new validator object"""
        self.test_validator = None

    def test_correct_data(self):
        """GetDocumentsValidatorTest: Given data is correct. No exceptions will be raised."""

        correct_data = {
            1: {
                "general": "I am a long, but very valid string",
                "publication_date": ["2020-12-3", "2020-12-3"],
                "tags": ["tag1", "tag2"]
            },

            2: {"general": "I am a long, but very valid string"},
            3: {"publication_date": ["2020-12-3", "2020-12-3"]},
            4: {"tags": ["tag1", "tag2"]},

            5:  {
                "general": "I am a long, but very valid string",
                "publication_date": [str(date.today()), str(date.today())]
            },

            6:  {
                "general": "I am a long, but very valid string",
                "tags": ["tag1", "tag2"]
            },

            7: {}
        }

        for x in range(1, len(correct_data) + 1):
            self.assertIsNotNone(self.test_validator.load(correct_data[x]))

    def test_incorrect_data(self):
        """ GetDocumentsValidatorTestTest: Given data is incorrect. ValidationError is raised"""

        incorrect_data = {
            1: {"general": 123},
            2: {"general": dict()},
            3: {"general": 0xFFFF},
            4: {"general": 0xFFFF},
            5: {"publication_date": []},
            6: {"publication_date": None},
            7: {"publication_date": [0, 0xFFFF]},
            8: {"publication_date": ["2020-12-3", None]},
            9: {"publication_date": [None, "2020-12-3"]},
            10: {"publication_date": [None, None]},
            11: {"tags": None},
            12: {"tags": []},
            13: {"tags": [0, 0]},
            14: {"tags": [123]}
        }

        for x in range(1, len(incorrect_data) + 1):
            with self.assertRaises(ValidationError):
                self.test_validator.load(incorrect_data[x])














