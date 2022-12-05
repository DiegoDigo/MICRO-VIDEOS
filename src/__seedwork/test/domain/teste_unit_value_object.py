import unittest
import uuid
from dataclasses import is_dataclass
from unittest.mock import patch

from src.__seedwork.domain.exceptions import InvalidUuidException
from src.__seedwork.domain.value_objects import UniqueEntityId


class TesteUnitValueObject(unittest.TestCase):
    def test_if_is_a_dataclass(self):
        self.assertTrue(is_dataclass(UniqueEntityId))  # add assertion here

    def teste_throw_exception_when_uuid_is_invalid(self):
        with patch.object(UniqueEntityId, '_UniqueEntityId__validate', autospec=True,
                          side_effect=UniqueEntityId._UniqueEntityId__validate) as mock_validate:
            with self.assertRaises(InvalidUuidException) as asserts_error:
                UniqueEntityId('fake id')
            mock_validate.assert_called_once()
            self.assertEqual(asserts_error.exception.args[0], 'ID must be a valid UUID')

    def teste_accept_uuid_passed_in_constructor(self):
        with patch.object(UniqueEntityId, '_UniqueEntityId__validate', autospec=True,
                          side_effect=UniqueEntityId._UniqueEntityId__validate) as mock_validate:
            value_object = UniqueEntityId('bfe239a0-cbdf-448d-ace1-5fa4b47cc8c5')
            mock_validate.assert_called_once()
            self.assertEqual(value_object.id, 'bfe239a0-cbdf-448d-ace1-5fa4b47cc8c5')

    def teste_genarate_id_when_no_passed_id_in_construct(self):
        with patch.object(UniqueEntityId, '_UniqueEntityId__validate', autospec=True,
                          side_effect=UniqueEntityId._UniqueEntityId__validate) as mock_validate:
            value_object = UniqueEntityId()
            uuid.UUID(value_object.id)
            mock_validate.assert_called_once()
