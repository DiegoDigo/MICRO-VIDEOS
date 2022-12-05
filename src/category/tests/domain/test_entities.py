import unittest
import uuid
from datetime import datetime
from dataclasses import is_dataclass

from src.category.domain.entities import Category


class TestCategory(unittest.TestCase):
    def test_if_is_a_dataclasse(self):
        self.assertTrue(is_dataclass(Category))

    def test_construct(self):
        category = Category(uuid.uuid4(), "Movie", 'some description', True, datetime.now())
        self.assertEqual(category.name, 'Movie')

    def test_if_created_at_is_generated_in_construct(self):
        category1 = Category("Movie 1")
        category2 = Category("Movie 2")

        self.assertNotEqual(category1.created_at, category2.created_at)